import os
from langchain_groq import ChatGroq

def get_llm():
    return ChatOpenAI(
        model=os.getenv("MODEL")
        temperature=0.0,  
        api_key=os.getenv("GROQ_API_KEY")
    )
