from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import setup_openai, process_direct_question

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Project Management Chatbot API",
    description="API for the Intelligent Projects Assistant Chatbot",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Gemini API
setup_openai()

# Pydantic models for request/response
class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle a chat question related to project management or project idea selection
    """
    try:
        response = process_direct_question(question=request.question)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))