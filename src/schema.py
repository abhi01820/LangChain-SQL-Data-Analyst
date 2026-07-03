import sqlite3

def get_schema(conn: sqlite3.Connection, table_name: str) -> str:
    try:
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        result = cursor.fetchone()
        
        if not result:
            raise ValueError(f"Table {table_name} not found in database.")
            
        create_statement = result[0]
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        
        schema_details = f"Table: {table_name}\n"
        schema_details += f"Schema:\n{create_statement}\n\nColumns:\n"
        
        for col in columns_info:
            col_name = col[1]
            col_type = col[2]
            schema_details += f"- {col_name} ({col_type})\n"
            
        return schema_details
    except Exception as e:
        raise ValueError(f"Error extracting schema: {e}")
