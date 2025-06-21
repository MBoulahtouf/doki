# src/doki/retrieval.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from . import config

def load_retriever():
    """
    Loads the vector store and returns a retriever object.
    """
    embedding_function = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
    db = Chroma(
        persist_directory=str(config.DB_PATH),
        embedding_function=embedding_function
    )
    return db.as_retriever(search_kwargs={"k": config.RETRIEVER_K})
