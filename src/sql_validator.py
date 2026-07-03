import sqlparse

def validate_sql_safety(query: str) -> bool:
    if not query or not query.strip():
        raise ValueError("Empty SQL query provided.")

    statements = sqlparse.split(query)
    statements = [stmt for stmt in statements if stmt.strip()]

    if len(statements) > 1:
        raise ValueError("Multiple SQL statements are not allowed for safety reasons.")
        
    statement = statements[0]
    parsed = sqlparse.parse(statement)[0]
    
    stmt_type = parsed.get_type().upper()
    
    allowed_types = ["SELECT", "WITH"]
    if stmt_type not in allowed_types:
        raise ValueError(f"Only SELECT or WITH queries are allowed. Found: {stmt_type}")
        
    forbidden_keywords = [
        "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE", 
        "EXEC", "EXECUTE", "MERGE", "GRANT", "REVOKE"
    ]
    
    for token in parsed.flatten():
        if token.is_keyword and token.value.upper() in forbidden_keywords:
             raise ValueError(f"Forbidden keyword '{token.value.upper()}' detected in query.")
             
    return True
