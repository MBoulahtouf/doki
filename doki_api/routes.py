# doki_api/routes.py
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.doki.chains import create_rag_chain

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

# Initialize the RAG chain
try:
    RAG_CHAIN = create_rag_chain()
    logging.info("RAG chain loaded successfully.")
except Exception as e:
    # If the chain fails to load (e.g., DB not found), we'll handle it gracefully
    RAG_CHAIN = None
    logging.error(f"FATAL: RAG chain failed to load: {e}", exc_info=True)


class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

def get_rag_chain():
    if not RAG_CHAIN:
        raise HTTPException(
            status_code=503,
            detail="RAG chain is not available. Check server logs. Has the data been ingested?"
        )
    return RAG_CHAIN

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_docs(request: ChatRequest, rag_chain = Depends(get_rag_chain)):
    """
    Receives a question and returns a RAG-generated answer from the documentation.
    """
    try:
        response = rag_chain.invoke({"input": request.question})
        answer = response.get("answer", "I couldn't find an answer in the provided documentation.")
        return ChatResponse(answer=answer)
    except Exception as e:
        logging.error(f"Error invoking RAG chain: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing the question.")
