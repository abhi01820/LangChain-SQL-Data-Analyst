from langchain_core.prompts import PromptTemplate
import pandas as pd
from .llm import get_llm

def generate_insights(df: pd.DataFrame, question: str) -> str:
    if df.empty:
        return "No data was returned for this query."
        
    data_sample = df.head(15).to_csv(index=False)
    
    prompt_template = """
You are a Data Analyst.
A user asked the following question: "{question}"

The SQL query returned the following data:
{data}

Provide a ONE-SENTENCE, factual, and strictly data-driven insight based ONLY on this returned data.
Do not invent business causes, unsupported explanations, or conversational filler.
Just state the most important visible pattern, maximum/minimum, or trend.

Insight:"""

    llm = get_llm()
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["question", "data"]
    )
    
    chain = prompt | llm
    
    try:
        insight = chain.invoke({"question": question, "data": data_sample})
        if hasattr(insight, 'content'):
            insight = insight.content
        return insight.strip()
    except Exception as e:
        return f"Could not generate insight automatically. (Data rows: {len(df)})"
