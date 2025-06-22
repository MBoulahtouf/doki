# src/doki/chains.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder
from . import config
from .retrieval import load_retriever

# Load environment variables from .env file
load_dotenv()

def create_rag_chain():
    """
    Creates and returns a history-aware RAG chain.
    """
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError(
            "GROQ_API_KEY environment variable is not set. "
            "Please set it with your Groq API key: export GROQ_API_KEY='your-api-key-here'"
        )
    
    retriever = load_retriever()
    llm = ChatGroq(model=config.LLM_MODEL_NAME)

    # 1. Prompt to rewrite the user's question with context
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    # Create history-aware retriever
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 2. Prompt for the final answer with chat history
    qa_system_prompt = """You are a helpful assistant for RamanSpy documentation.
    
    Your task is to answer the user's question based on the provided context and chat history.
    
    Synthesize a comprehensive answer from the context chunks given below.
    If the context does not contain the information needed to answer the question,
    state that you couldn't find specific information in the documentation.
    
    Do not make up information.
    
    <context>
    {context}
    </context>
    
    Chat History:
    <chat_history>
    {chat_history}
    </chat_history>
    
    Question: {input}
    """
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            ("human", "{input}"),
        ]
    )

    # Create the document chain with history-aware prompt
    document_chain = create_stuff_documents_chain(llm, qa_prompt)

    # Create the final RAG chain
    rag_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    return rag_chain