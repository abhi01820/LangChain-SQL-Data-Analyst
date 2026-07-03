from langchain_core.prompts import PromptTemplate
import re
from .llm import get_llm

def generate_sql(question: str, schema: str) -> str:
    llm = get_llm()
    
    prompt_template = """
You are an expert SQL Data Analyst.
Given the following SQLite database schema, write a SQL query to answer the user's question.

IMPORTANT RULES:
- Generate ONLY valid SQLite-compatible SQL.
- Use only the tables and columns provided in the schema. Do not invent columns.
- Return ONLY the SQL query. Do not include any explanations or conversational text.
- Do NOT wrap the SQL in markdown code fences (like ```sql or ```).
- Generate read-only SELECT queries.

{schema}

User Question: {question}

SQL Query:"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["schema", "question"]
    )
    
    chain = prompt | llm
    raw_response = chain.invoke({"schema": schema, "question": question})
    
    if hasattr(raw_response, 'content'):
        raw_response = raw_response.content
        
    return clean_sql_output(raw_response)

def clean_sql_output(raw_sql: str) -> str:
    cleaned = raw_sql.strip()
    if cleaned.startswith("```sql"):
        cleaned = cleaned[6:]
    elif cleaned.startswith("```"):
         cleaned = cleaned[3:]
         
    if cleaned.endswith("```"):
         cleaned = cleaned[:-3]
         
    cleaned = cleaned.strip()
    return cleaned
