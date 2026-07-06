import logging
import json
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.security import security_guardrail
from agents.router import get_router
from models.schemas import ChatRequest, ChatResponse, VocabResponse
from dotenv import load_dotenv

from database.database import engine, Base, get_db
from database import crud

load_dotenv()

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Smart English Concierge API")

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Setup CORS
allowed_origins = [
    "http://localhost:5173",               # Vite dev server
    "http://localhost:3000",               # Alternative local dev
    "https://smart-english-frontend-183082507811.asia-southeast1.run.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the router (This will auto-scan skills/ and initialize the real Gemini SDK)
router_instance = get_router()

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main entry point for chat requests.
    1. Sanitizes input using security_guardrail (Prompt Injection & PII protection).
    2. Routes the sanitized input to the appropriate AI agent/skill.
    3. Returns the structured response back to the frontend.
    """
    try:

        logger.info("=" * 60)
        logger.info("Original message:")
        logger.info(request.message)
        # Step 1: Security Guardrail Check
        is_safe, sanitized_message = security_guardrail(request.message)
        logger.info("Sanitized message:")
        logger.info(sanitized_message)
        logger.info(f"Is safe: {is_safe}")
        logger.info("=" * 60)
        if not is_safe:
            logger.warning(f"Security Alert: {sanitized_message}")
            return ChatResponse(
                status="error",
                message=sanitized_message,
                skill="security_guardrail"
            )
            
        # Step 2: Route through the Agent Graph via LLM Tool Calling
        # (This uses the real Gemini API initialized in the router)
        result = await router_instance.route(sanitized_message)
        
        # Extract status and message from the result properly
        # The result might look like {"status": "success", "skill": "vocab-saver", "data": {...}}
        # Or {"status": "default", "message": "..."}
        
        response_msg = result.get("message", "")
        if not response_msg and "data" in result and isinstance(result["data"], dict):
            # If the handler returned a message inside 'data'
            response_msg = result["data"].get("message", "Request processed successfully.")
            
        return ChatResponse(
            status=result.get("status", "unknown"),
            message=response_msg,
            skill=result.get("skill"),
            data=result.get("data")
        )
        
    except Exception as e:
        logger.exception("Error processing chat request")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api/vocabulary", response_model=VocabResponse)
def get_vocabulary(db: Session = Depends(get_db)):
    """Returns all saved vocabulary words."""
    try:
        words = crud.get_all_vocabulary(db)
        
        # Convert SQLAlchemy models to dicts
        word_list = [
            {
                "id": w.id,
                "word": w.word,
                "meaning": w.meaning,
                "example": w.example,
                "created_at": w.created_at.isoformat() if w.created_at else None
            }
            for w in words
        ]
        
        return VocabResponse(status="success", words=word_list)
    except Exception as e:
        logger.exception("Error reading vocabulary from database")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
