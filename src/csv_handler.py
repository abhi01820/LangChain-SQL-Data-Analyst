import pandas as pd
import re
import os

def clean_column_name(col_name: str) -> str:
    col_name = str(col_name)
    col_name = col_name.strip()
    col_name = col_name.replace(" ", "_")
    col_name = re.sub(r'[^a-zA-Z0-9_]', '', col_name)
    if col_name and col_name[0].isdigit():
        col_name = "col_" + col_name
    return col_name.lower()

def load_and_clean_csv(file_path_or_buffer) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path_or_buffer)
        df.columns = [clean_column_name(col) for col in df.columns]
        return df
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {e}")
