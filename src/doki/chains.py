# src/doki/chains.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from . import config
from .retrieval import load_retriever

# Load environment variables from .env file
load_dotenv()

def create_rag_chain():
    """
    Creates and returns the full RAG chain.
    """
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY environment variable is not set. "
            "Please set it with your Groq API key: export GROQ_API_KEY='your-api-key-here'"
        )
    
    retriever = load_retriever()
    prompt = ChatPromptTemplate.from_template(config.PROMPT_TEMPLATE)
    llm = ChatGroq(model=config.LLM_MODEL_NAME)

    Youtube_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, Youtube_chain)

    return rag_chain