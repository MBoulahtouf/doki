# src/doki/config.py
from pathlib import Path

# --- DIRECTORIES ---
BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR / "data" / "chroma_db"

# --- EMBEDDING & LLM MODELS ---
EMBEDDING_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL_NAME = "llama3-8b-8192"

# --- RAG ---
# Number of context chunks to retrieve
RETRIEVER_K = 5

# Prompt template for the RAG chain
PROMPT_TEMPLATE = """
You are a helpful assistant.
Your task is to answer the user's question based on the provided context.

Synthesize a comprehensive answer from the context chunks given below.
If the context does not contain the information needed to answer the question,
state that you couldn't find specific information in the documentation.

Do not make up information.

<context>
{context}
</context>

Question: {input}
"""
