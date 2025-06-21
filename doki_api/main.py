# doki_api/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
from . import routes

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Doki - Chat with Docs API",
    description="An API for chatting with technical documentation using RAG.",
    version="0.1.0"
)

# Include the chat routes
app.include_router(routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Doki API!"}
