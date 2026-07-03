import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
         raise ValueError("GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")

    # Using gemini-2.5-flash which is confirmed to be available on your API key
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        google_api_key=api_key
    )
    
    return llm
