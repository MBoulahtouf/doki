# doki_api/routes.py
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from src.doki.chains import create_rag_chain

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

# --- Pydantic Models for API I/O ---
class ChatRequest(BaseModel):
    question: str
    chat_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    answer: str

# --- Dependency to get the RAG chain ---
# This ensures the chain is loaded only once and is available to the endpoint.
try:
    RAG_CHAIN = create_rag_chain()
    logging.info("RAG chain loaded successfully.")
except Exception as e:
    # If the chain fails to load (e.g., DB not found), we'll handle it gracefully
    RAG_CHAIN = None
    logging.error(f"FATAL: RAG chain failed to load: {e}", exc_info=True)

def get_rag_chain():
    if not RAG_CHAIN:
        raise HTTPException(
            status_code=503,
            detail="RAG chain is not available. Check server logs. Has the data been ingested?"
        )
    return RAG_CHAIN

# --- API Endpoint ---
@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_docs(request: ChatRequest, rag_chain = Depends(get_rag_chain)):
    """
    Receives a question and chat history, returns a RAG-generated answer from the documentation.
    """
    try:
        # Prepare the input for the history-aware RAG chain
        chain_input = {
            "input": request.question,
            "chat_history": request.chat_history or []
        }
        
        response = rag_chain.invoke(chain_input)
        answer = response.get("answer", "I couldn't find an answer in the provided documentation.")
        return ChatResponse(answer=answer)
    except Exception as e:
        logging.error(f"Error invoking RAG chain: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the question.")
