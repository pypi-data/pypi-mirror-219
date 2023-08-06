import duckdb


DUCKDB_MEMORY_CONN = None


def duckdb_cursor():
    global DUCKDB_MEMORY_CONN
    if DUCKDB_MEMORY_CONN is None:
        DUCKDB_MEMORY_CONN = duckdb.connect(":memory:")

    return DUCKDB_MEMORY_CONN.cursor()


def quote_sql_string(s):
    return "'" + str(s).replace("'", "''") + "'"


def quote_sql_ident(s, suffix=""):
    return '"' + (str(s) + suffix).replace('"', '""') + '"'
