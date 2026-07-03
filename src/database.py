import sqlite3
import pandas as pd

def create_connection(db_file: str = ":memory:"):
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Exception as e:
        raise ConnectionError(f"Failed to connect to SQLite database: {e}")

def load_df_to_sqlite(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection):
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    except Exception as e:
        raise ValueError(f"Failed to load DataFrame to SQLite: {e}")

def execute_query(query: str, conn: sqlite3.Connection) -> pd.DataFrame:
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        raise ValueError(f"Query execution failed: {e}")
