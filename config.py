import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Get API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize Groq LLM
def get_llm():
    return ChatGroq(
        model_name = "llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=GROQ_API_KEY
    )