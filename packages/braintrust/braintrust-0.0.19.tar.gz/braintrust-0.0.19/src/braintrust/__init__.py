"""
A Python library for logging data to BrainTrust.

### Quickstart

Install the library with pip.

```bash
pip install braintrust
```

Then, run a simple experiment with the following code (replace `YOUR_API_KEY` with
your BrainTrust API key):

```python
import braintrust

experiment = braintrust.init(project="PyTest", api_key="YOUR_API_KEY")
experiment.log(
    inputs={"test": 1},
    output="foo",
    expected="bar",
    scores={
        "n": 0.5,
    },
    metadata={
        "id": 1,
    },
)
print(experiment.summarize())
```

### API Reference
"""
import atexit
import dataclasses
import datetime
import json
import logging
import os
import queue
import textwrap
import threading
import traceback
import urllib.parse
import uuid
from functools import cache as _cache
from getpass import getpass
from typing import Any, Dict, Optional

import duckdb
import git
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .cache import CACHE_PATH, EXPERIMENTS_PATH, LOGIN_INFO_PATH
from .duckutil import duckdb_cursor, quote_sql_ident, quote_sql_string
from .gitutil import get_past_n_ancestors, get_repo_status
from .oai import run_cached_request
from .util import SerializableDataClass


class BrainTrustState:
    def __init__(self):
        self.current_project = None
        self.current_experiment = None


_state = BrainTrustState()
_logger = logging.getLogger("braintrust")

API_URL = None
ORG_ID = None
ORG_NAME = None
LOG_URL = None
LOGGED_IN = False


class HTTPConnection:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

        self._reset(total=0)

    def ping(self):
        try:
            resp = self.get("ping")
            return resp.ok
        except requests.exceptions.ConnectionError:
            return False

    def make_long_lived(self):
        # Following a suggestion in https://stackoverflow.com/questions/23013220/max-retries-exceeded-with-url-in-requests
        self._reset(connect=10, backoff_factor=0.5)

    def set_token(self, token):
        token = token.rstrip("\n")
        self.token = token
        self._set_session_token()

    def _reset(self, **retry_kwargs):
        self.session = requests.Session()

        retry = Retry(**retry_kwargs)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self._set_session_token()

    def _set_session_token(self):
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def get(self, path, *args, **kwargs):
        return self.session.get(_urljoin(self.base_url, path), *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.session.post(_urljoin(self.base_url, path), *args, **kwargs)


@_cache
def api_conn():
    return HTTPConnection(LOG_URL)  # TODO: Fix to use global install


def api_get(object_type, args=None):
    resp = api_conn().get(f"/{object_type}", params=args)
    resp.raise_for_status()
    return resp.json()


def api_insert(object_type, args):
    resp = api_conn().post(
        f"/{object_type}",
        json=args,
    )
    resp.raise_for_status()
    return resp.json()


class ModelWrapper:
    _ENDPOINT = None

    def __getattr__(self, name: str) -> Any:
        return self.data[name]


@_cache
def _user_info():
    return api_get("ping")


class Project(ModelWrapper):
    _ENDPOINT = "projects"

    def __init__(self, name):
        unique_key = {"name": name, "org_id": ORG_ID}

        # Can we have an upsert (or insert if not exists) method instead?
        existing = []
        if unique_key:
            existing = api_get(self._ENDPOINT, unique_key)

        if not existing:
            existing = api_insert(self._ENDPOINT, unique_key)

        if existing:
            self.data = existing[0]
        else:
            assert False, "Unable to find record in " + self._ENDPOINT


def guess_notebook_block_name():
    try:
        import IPython

        ipython = IPython.get_ipython()

        cell_text = "\n".join(reversed([ipython.history_manager.get_tail(i + 1)[0][2] for i in range(3)]))
    except Exception:
        return None

    return [
        {
            "role": "system",
            "content": """\
You can generate two word summaries for machine learning experiment names, based
on the last 3 blocks of code in your notebook.
The experiment name should be exactly two words, concatenated with a hyphen, all lowercase.
The input format is recently executed python code. For example, "foo-bar" is valid but
"foo-bar-baz" is not.""",
        },
        {
            "role": "user",
            "content": f"{cell_text[:4096]}",
        },
    ]


def guess_git_experiment_name():
    try:
        repo = git.Repo(search_parent_directories=True)
    except git.InvalidGitRepositoryError:
        return None

    branch = repo.active_branch.name
    diff = repo.git.diff(repo.head.commit.tree)
    if not diff and len(repo.head.commit.parents) > 0:
        diff = repo.head.commit.message + "\n" + repo.git.diff(repo.head.commit.tree, repo.head.commit.parents[0].tree)

    return [
        {
            "role": "system",
            "content": """\
You can generate two word summaries for machine learning experiment names, based
on the branch name and an optional "diff" of the experiment's code on top of the branch.
The experiment name should be exactly two words, concatenated with a hyphen, all lowercase.
The input format is the output of "git diff". For example, "foo-bar" is valid but
"foo-bar-baz" is not.""",
        },
        {
            "role": "user",
            "content": f"Branch: {branch}" + (f"\n\nDiff:\n{diff[:4096]}" if diff else ""),
        },
    ]


def guess_experiment_name():
    # OpenAI is very slow to import, so we only do it when we need it
    import openai

    if openai.api_key is None:
        return None

    messages = guess_notebook_block_name()
    if not messages:
        messages = guess_git_experiment_name()

    if not messages:
        return None

    resp = run_cached_request(
        Completion=openai.ChatCompletion,
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=128,
        temperature=0.7,
    )

    name = None
    if len(resp["choices"]) > 0:
        name = "-".join(resp["choices"][0]["message"]["content"].split("-")[:2])
        # Strip punctuation and whitespace from the prefix and suffix
        name = name.strip(" .,;:!?-")
    return name


class _LogThread:
    def __init__(self, local_json_path, name=None):
        self.thread = threading.Thread(target=self._publisher, daemon=True)
        self.started = False

        log_namespace = "braintrust"
        if name:
            log_namespace += f" [{name}]"

        self.logger = logging.getLogger(log_namespace)

        try:
            queue_size = int(os.environ.get("BRAINTRUST_QUEUE_SIZE"))
        except Exception:
            queue_size = 1000
        self.queue = queue.Queue(maxsize=queue_size)

        os.makedirs(EXPERIMENTS_PATH, exist_ok=True)
        self.local_json = open(local_json_path, "w")

        atexit.register(self._finalize)

    def log(self, *args):
        self._start()
        for event in args:
            self.queue.put(event)

    def _start(self):
        if not self.started:
            self.thread.start()
            self.started = True

    def _finalize(self):
        self.logger.info("Flushing final log events...")
        self.flush()

    def _publisher(self, batch_size=None):
        kwargs = {}
        if batch_size is not None:
            kwargs["batch_size"] = batch_size

        while True:
            try:
                item = self.queue.get()
            except queue.Empty:
                continue

            try:
                self.flush(initial_items=[item], **kwargs)
            except Exception:
                traceback.print_exc()

    def flush(self, initial_items=None, batch_size=100):
        items = initial_items or []
        while True:
            while len(items) < batch_size:
                try:
                    items.append(self.queue.get_nowait())
                except queue.Empty:
                    break

            if len(items) > 0:
                print("\n".join([json.dumps(item) for item in items]), file=self.local_json)
                self.local_json.flush()
                api_insert("logs", items)

            if len(items) < batch_size:
                break

            items.clear()


def _ensure_experiment(experiment_id, force=False):
    experiment_path = EXPERIMENTS_PATH / f"{experiment_id}.parquet"

    if force or not experiment_path.exists():
        os.makedirs(EXPERIMENTS_PATH, exist_ok=True)
        conn = api_conn()
        resp = conn.get(
            "experiment",
            params={"experiment_id": experiment_id},
            headers={
                "Accept": "application/octet-stream",
            },
        )

        with open(experiment_path, "wb") as f:
            f.write(resp.content)

    return experiment_path


def init(
    project,
    experiment=None,
    description=None,
    base_experiment=None,
    api_url=None,
    api_key=None,
    org_name=None,
    disable_cache=False,
):
    """
    Log in, and then initialize a new experiment in a specified project. If the project does not exist, it will be created.

    :param project: The name of the project to create the experiment in.
    :param experiment: The name of the experiment to create. If not specified, a name will be generated automatically.
    :param description: An optional description of the experiment.
    :param base_experiment: An optional experiment name to use as a base. If specified, the new experiment will be summarized and compared to this
    experiment. Otherwise, it will pick an experiment by finding the closest ancestor on the default (e.g. main) branch.
    :param api_url: The URL of the BrainTrust API. Defaults to https://www.braintrustdata.com.
    :param api_key: The API key to use. If the parameter is not specified, will try to use the `BRAINTRUST_API_KEY` environment variable. If no API
    key is specified, will prompt the user to login.
    :param org_name: (Optional) The name of a specific organization to connect to. This is useful if you belong to multiple.
    :param disable_cache: Do not use cached login information.
    :returns: The experiment object.
    """
    login(org_name=org_name, disable_cache=disable_cache, api_key=api_key, api_url=api_url)

    _state.current_project = Project(project)
    _state.current_experiment = Experiment(
        _state.current_project, name=experiment, description=description, base_experiment=base_experiment
    )
    return _state.current_experiment


def log(inputs, output, expected, scores, metadata=None):
    """
    Log a single event to the current experiment. The event will be batched and uploaded behind the scenes.

    :param inputs: The arguments that uniquely define a test case (an arbitrary, JSON serializable object). Later on,
    BrainTrust will use the `inputs` to know whether two test casess are the same between experiments, so they should
    not contain experiment-specific state. A simple rule of thumb is that if you run the same experiment twice, the
    `inputs` should be identical.
    :param output: The output of your application, including post-processing (an arbitrary, JSON serializable object),
    that allows you to determine whether the result is correct or not. For example, in an app that generates SQL queries,
    the `output` should be the _result_ of the SQL query generated by the model, not the query itself, because there may
    be multiple valid queries that answer a single question.
    :param expected: The ground truth value (an arbitrary, JSON serializable object) that you'd compare to `output` to
    determine if your `output` value is correct or not. BrainTrust currently does not compare `output` to `expected` for
    you, since there are so many different ways to do that correctly. Instead, these values are just used to help you
    navigate your experiments while digging into analyses. However, we may later use these values to re-score outputs or
    fine-tune your models.
    :param scores: A dictionary of numeric values (between 0 and 1) to log. The scores should give you a variety of signals
    that help you determine how accurate the outputs are compared to what you expect and diagnose failures. For example, a
    summarization app might have one score that tells you how accurate the summary is, and another that measures the word similarity
    between the generated and grouth truth summary. The word similarity score could help you determine whether the summarization was
    covering similar concepts or not. You can use these scores to help you sort, filter, and compare experiments.
    :param metadata: (Optional) a dictionary with additional data about the test example, model outputs, or just
    about anything else that's relevant, that you can use to help find and analyze examples later. For example, you could log the
    `prompt`, example's `id`, or anything else that would be useful to slice/dice later. The values in `metadata` can be any
    JSON-serializable type, but its keys must be strings.
    :returns: The `id` of the logged event.
    """

    if not _state.current_experiment:
        raise Exception("Not initialized. Please call init() or login() first")

    return _state.current_experiment.log(
        inputs=inputs, output=output, expected=expected, scores=scores, metadata=metadata
    )


def login(api_url=None, api_key=None, org_name=None, disable_cache=False, force_login=False):
    """
    Log into BrainTrust. This will prompt you for your API token, which you can find at
    https://www.braintrustdata.com/app/token. This method is called automatically by `init()`.

    :param api_url: The URL of the BrainTrust API. Defaults to https://www.braintrustdata.com.
    :param api_key: The API key to use. If the parameter is not specified, will try to use the `BRAINTRUST_API_KEY` environment variable. If no API
    key is specified, will prompt the user to login.
    :param org_name: (Optional) The name of a specific organization to connect to. This is useful if you belong to multiple.
    :param disable_cache: Do not use cached login information.
    :param force_login: Login again, even if you have already logged in (by default, this function will exit quickly if you have already logged in)
    """

    global API_URL, ORG_ID, ORG_NAME, LOG_URL, LOGGED_IN
    if not force_login and LOGGED_IN:
        # We have already logged in
        return

    if api_url is None:
        api_url = os.environ.get("BRAINTRUST_API_URL", "https://www.braintrustdata.com")

    if api_key is None:
        api_key = os.environ.get("BRAINTRUST_API_KEY")

    API_URL = api_url

    login_key_info = None
    ping_ok = False

    os.makedirs(CACHE_PATH, exist_ok=True)

    if api_key is not None:
        resp = requests.post(_urljoin(API_URL, "/api/apikey/login"), json={"token": api_key})
        resp.raise_for_status()
        info = resp.json()

        _check_org_info(info["org_info"], org_name)

        conn = api_conn()
        conn.set_token(api_key)

        ping_ok = conn.ping()

    if not ping_ok and os.path.exists(LOGIN_INFO_PATH) and not disable_cache:
        with open(LOGIN_INFO_PATH) as f:
            login_key_info = json.load(f)

        LOG_URL = login_key_info.get("log_url")
        ORG_ID = login_key_info.get("org_id")
        ORG_NAME = login_key_info.get("org_name")
        conn = api_conn()

        token = login_key_info.get("token")
        if token is not None:
            conn.set_token(token)

        ping_ok = conn.ping()

    # TODO: This logic should likely be removed permanently, because the use of refresh tokens
    # has been superseded by API keys. However, I'm leaving it here for now in case we revisit
    # that in the near term.
    #
    #    if not ping_ok and login_key_info and login_key_info.get("refresh_token"):
    #        resp = requests.post(
    #            _urljoin(API_URL, "/api/token/refresh"), json={"refresh_token": login_key_info.get("refresh_token")}
    #        )
    #        if resp.ok:
    #            resp_data = resp.json()
    #            token = resp_data["id_token"]
    #            refresh_token = resp_data.get("refresh_token")
    #
    #            if not disable_cache:
    #                _save_api_info({**login_key_info, "token": token, "refresh_token": refresh_token})
    #
    #            conn.set_token(token)
    #            ping_ok = conn.ping()
    #        else:
    #            _logger.warning(f"Failed to refresh token: [{resp.status_code}] {resp.text}")

    if not ping_ok or ORG_ID is None or ORG_NAME is None or LOG_URL is None:
        print(
            textwrap.dedent(
                f"""\
            The recommended way to login is to generate an API token at {API_URL}/app/settings.
            However, BrainTrust also supports generating a temporary token for the SDK. This token
            will expire after about an hour, so it is not recommended for long-term use.

            Please copy your temporary token from {API_URL}/app/token."""
            )
        )
        temp_token = getpass("Token: ")

        resp = requests.post(_urljoin(API_URL, "/api/id-token"), json={"token": temp_token})
        resp.raise_for_status()
        info = resp.json()
        token = info["token"]

        _check_org_info(info["org_info"], org_name)

        if not disable_cache:
            _save_api_info({"token": token, "org_id": ORG_ID, "log_url": LOG_URL, "org_name": ORG_NAME})

        conn = api_conn()
        conn.set_token(token)

        ping_ok = conn.ping()

    assert conn, "Conn should be set at this point (a bug)"

    # Do not use the "ping" method here, because we'd like to `raise_for_status()` in case
    # of any remaining errors.
    if not ping_ok:
        # Try to produce a more informative error message. If we do somehow succeed here, then
        # we can safely assume that the connection is working.
        resp = conn.get("ping")
        resp.raise_for_status()

    # make_long_lived() allows the connection to retry if it breaks, which we're okay with after
    # this point because we know the connection _can_ successfully ping.
    conn.make_long_lived()
    LOGGED_IN = True


def summarize(summarize_scores=True, comparison_experiment_id=None):
    """
    Summarize the current experiment, including the scores (compared to the closest reference experiment) and metadata.

    :param summarize_scores: Whether to summarize the scores. If False, only the metadata will be returned.
    :param comparison_experiment_id: The experiment to compare against. If None, the most recent experiment on the comparison_commit will be used.
    :returns: `ExperimentSummary`
    """
    if not _state.current_experiment:
        raise Exception("Not initialized. Please call init() first")

    return _state.current_experiment.summarize(
        summarize_scores=summarize_scores,
        comparison_experiment_id=comparison_experiment_id,
    )


def _check_org_info(org_info, org_name):
    global ORG_ID, ORG_NAME, LOG_URL

    if len(org_info) == 0:
        raise ValueError("This user is not part of any organizations.")

    for orgs in org_info:
        if org_name is None or orgs["name"] == org_name:
            ORG_ID = orgs["id"]
            ORG_NAME = orgs["name"]
            LOG_URL = orgs["api_url"]
            break

    if ORG_ID is None:
        raise ValueError(
            f"Organization {org_name} not found. Must be one of {', '.join([x['name'] for x in org_info])}"
        )


def _save_api_info(api_info):
    os.makedirs(CACHE_PATH, exist_ok=True)
    with open(LOGIN_INFO_PATH, "w") as f:
        json.dump(api_info, f)


def _urljoin(*parts):
    return "/".join([x.lstrip("/") for x in parts])


class Experiment(ModelWrapper):
    """
    An experiment is a collection of logged events, such as model inputs and outputs, which represent
    a snapshot of your application at a particular point in time. An experiment is meant to capture more
    than just the model you use, and includes the data you use to test, pre- and post- processing code,
    comparison metrics (scores), and any other metadata you want to include.

    Experiments are associated with a project, and two experiments are meant to be easily comparable via
    their `inputs`. You can change the attributes of the experiments in a project (e.g. scoring functions)
    over time, simply by changing what you log.

    You should not create `Experiment` objects directly. Instead, use the `braintrust.init()` method.
    """

    def __init__(self, project: Project, name: str = None, description: str = None, base_experiment: str = None):
        self.project = project
        args = {"project_id": project.id}

        if not name:
            name = guess_experiment_name()

        if name:
            args["name"] = name

        if description:
            args["description"] = description

        repo_status = get_repo_status()
        if repo_status:
            args["repo_info"] = repo_status.as_dict()

        conn = api_conn()
        base_exp_id = None
        if base_experiment is not None:
            resp = conn.get("experiments", params={"project_id": project.id, "name": base_experiment})
            resp.raise_for_status()
            experiments = resp.json()
            if len(experiments) > 0:
                base_exp_id = experiments[0]["id"]
            else:
                raise ValueError(f"Base experiment {base_experiment} not found")

        if base_exp_id is None:
            resp = conn.post(
                "experiments-by-commits", json={"project_id": project.id, "commits": list(get_past_n_ancestors())}
            )
            resp.raise_for_status()
            base_exp_id = resp.json()["experiment_id"]

        args["base_exp_id"] = base_exp_id

        self.data = api_insert("register-experiment", args)[0]

        self.local_json_path = EXPERIMENTS_PATH / f"{self.id}.json"
        self.local_parquet_path = EXPERIMENTS_PATH / f"{self.id}.parquet"
        self.logger = _LogThread(local_json_path=self.local_json_path, name=name)

    def log(self, inputs, output, expected, scores, metadata=None):
        """
        Log a single event to the experiment. The event will be batched and uploaded behind the scenes.

        :param inputs: The arguments that uniquely define a test case (an arbitrary, JSON serializable object). Later on,
        BrainTrust will use the `inputs` to know whether two test casess are the same between experiments, so they should
        not contain experiment-specific state. A simple rule of thumb is that if you run the same experiment twice, the
        `inputs` should be identical.
        :param output: The output of your application, including post-processing (an arbitrary, JSON serializable object),
        that allows you to determine whether the result is correct or not. For example, in an app that generates SQL queries,
        the `output` should be the _result_ of the SQL query generated by the model, not the query itself, because there may
        be multiple valid queries that answer a single question.
        :param expected: The ground truth value (an arbitrary, JSON serializable object) that you'd compare to `output` to
        determine if your `output` value is correct or not. BrainTrust currently does not compare `output` to `expected` for
        you, since there are so many different ways to do that correctly. Instead, these values are just used to help you
        navigate your experiments while digging into analyses. However, we may later use these values to re-score outputs or
        fine-tune your models.
        :param scores: A dictionary of numeric values (between 0 and 1) to log. The scores should give you a variety of signals
        that help you determine how accurate the outputs are compared to what you expect and diagnose failures. For example, a
        summarization app might have one score that tells you how accurate the summary is, and another that measures the word similarity
        between the generated and grouth truth summary. The word similarity score could help you determine whether the summarization was
        covering similar concepts or not. You can use these scores to help you sort, filter, and compare experiments.
        :param metadata: (Optional) a dictionary with additional data about the test example, model outputs, or just
        about anything else that's relevant, that you can use to help find and analyze examples later. For example, you could log the
        `prompt`, example's `id`, or anything else that would be useful to slice/dice later. The values in `metadata` can be any
        JSON-serializable type, but its keys must be strings.
        :returns: The `id` of the logged event.
        """

        user_id = _user_info()["id"]

        if not isinstance(scores, dict):
            raise ValueError("scores must be a dictionary of names with scores")
        for name, score in scores.items():
            if not isinstance(name, str):
                raise ValueError("score names must be strings")
            if not isinstance(score, (int, float)):
                raise ValueError("score values must be numbers")
            if score < 0 or score > 1:
                raise ValueError("score values must be between 0 and 1")

        if metadata:
            if not isinstance(metadata, dict):
                raise ValueError("metadata must be a dictionary")
            for key in metadata.keys():
                if not isinstance(key, str):
                    raise ValueError("metadata keys must be strings")

        args = {
            "id": str(uuid.uuid4()),
            "inputs": inputs,
            "output": output,
            "expected": expected,
            "scores": scores,
            "project_id": self.project.id,
            "experiment_id": self.id,
            "user_id": user_id,
            "created": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        if metadata:
            args["metadata"] = metadata

        if len(json.dumps(args)) >= 65535:
            raise ValueError(
                "Events must be less than 64KB in size. Please reduce the size of your inputs, output, expected, scores, or metadata."
            )

        self.logger.log(args)
        return args["id"]

    def summarize(self, summarize_scores=True, comparison_experiment_id=None):
        """
        Summarize the experiment, including the scores (compared to the closest reference experiment) and metadata.

        :param summarize_scores: Whether to summarize the scores. If False, only the metadata will be returned.
        :param comparison_experiment_id: The experiment to compare against. If None, the most recent experiment on the origin's main branch will be used.
        :returns: `ExperimentSummary`
        """

        # Flush our events to the API, and to the data warehouse, to ensure that the link we print
        # includes the new experiment.
        self.logger.flush()

        project_url = f"{API_URL}/app/{urllib.parse.quote(ORG_NAME)}/p/{urllib.parse.quote(self.project.name)}"
        experiment_url = f"{project_url}/{urllib.parse.quote(self.name)}"

        score_summary = {}
        comparison_experiment_name = None
        if summarize_scores:
            # Get the comparison experiment
            if comparison_experiment_id is None:
                conn = api_conn()
                resp = conn.get("/crud/base_experiments", params={"id": self.id})
                resp.raise_for_status()
                base_experiments = resp.json()
                if base_experiments:
                    comparison_experiment_id = base_experiments[0]["base_exp_id"]
                    comparison_experiment_name = base_experiments[0]["base_exp_name"]

            if comparison_experiment_id is not None:
                summary_items = conn.get(
                    "/experiment-comparison",
                    params={
                        "experiment_id": self.id,
                        "base_experiment_id": comparison_experiment_id,
                    },
                ).json()
                longest_score_name = max(len(k) for k in summary_items.keys())
                score_summary = {
                    k: ScoreSummary(_longest_score_name=longest_score_name, **v) for (k, v) in summary_items.items()
                }

        return ExperimentSummary(
            project_name=self.project.name,
            experiment_name=self.name,
            project_url=project_url,
            experiment_url=experiment_url,
            comparison_experiment_name=comparison_experiment_name,
            scores=score_summary,
        )


@dataclasses.dataclass
class ScoreSummary(SerializableDataClass):
    """Summary of a score's performance."""

    """Name of the score."""
    name: str
    """Average score across all examples."""
    score: float
    """Difference in score between the current and reference experiment."""
    diff: float
    """Number of improvements in the score."""
    improvements: int
    """Number of regressions in the score."""
    regressions: int

    # Used to help with formatting
    _longest_score_name: int

    def __str__(self):
        # format with 2 decimal points and pad so that it's exactly 2 characters then 2 decimals
        score_pct = f"{self.score * 100:05.2f}%"
        diff_pct = f"{abs(self.diff) * 100:05.2f}%"
        diff_score = f"+{diff_pct}" if self.diff > 0 else f"-{diff_pct}" if self.diff < 0 else "-"

        # pad the name with spaces so that its length is self._longest_score_name + 2
        score_name = f"'{self.name}'".ljust(self._longest_score_name + 2)

        return textwrap.dedent(
            f"""{score_pct} ({diff_score}) {score_name} score\t({self.improvements} improvements, {self.regressions} regressions)"""
        )


@dataclasses.dataclass
class ExperimentSummary(SerializableDataClass):
    """Summary of an experiment's scores and metadata."""

    """Name of the project that the experiment belongs to."""
    project_name: str
    """Name of the experiment."""
    experiment_name: str
    """URL to the project's page in the BrainTrust app."""
    project_url: str
    """URL to the experiment's page in the BrainTrust app."""
    experiment_url: str
    """The experiment scores are baselined against."""
    comparison_experiment_name: Optional[str]
    """Summary of the experiment's scores."""
    scores: Dict[str, ScoreSummary]

    def __str__(self):
        comparison_line = ""
        if self.comparison_experiment_name:
            comparison_line = f"""{self.experiment_name} compared to {self.comparison_experiment_name}:\n"""
        return (
            f"""\n=========================SUMMARY=========================\n{comparison_line}"""
            + "\n".join([str(score) for score in self.scores.values()])
            + ("\n\n" if self.scores else "")
            + textwrap.dedent(
                f"""\
        See results for all experiments in {self.project_name} at {self.project_url}
        See results for {self.experiment_name} at {self.experiment_url}"""
            )
        )


__all__ = ["init", "log", "login"]
