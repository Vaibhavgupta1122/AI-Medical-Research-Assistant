from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import json
import os
from typing import List, Dict, Any
from ollama_client import ollama_client

app = FastAPI(title="AI Medical Research Service")

class ResearchRequest(BaseModel):
    query: str
    context: Dict[str, Any] = {}
    conversation_history: List[Dict[str, Any]] = []

class ResearchResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float

@app.get("/")
async def root():
    return {
        "message": "AI Medical Research Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "research": "/research (POST)",
            "docs": "/docs (Swagger UI)",
            "redoc": "/redoc (ReDoc)"
        }
    }

@app.get("/health")
async def health_check():
    ollama_status = await ollama_client.check_connection()
    available_models = await ollama_client.get_available_models()
    
    return {
        "status": "healthy",
        "service": "AI Medical Research Service",
        "ollama": {
            "connected": ollama_status,
            "available_models": available_models,
            "current_model": ollama_client.model
        }
    }

@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    try:
        # Check if Ollama is available
        ollama_connected = await ollama_client.check_connection()
        
        if not ollama_connected:
            # Fallback response if Ollama is not available
            answer = f"""I apologize, but I cannot connect to the AI service (Ollama) at the moment. 

To fix this:
1. Make sure Ollama is installed and running: `ollama serve`
2. Ensure the Mistral model is available: `ollama pull mistral`
3. Check if Ollama is accessible at http://localhost:11434

Your query was: "{request.query}"

Once Ollama is properly configured, I'll be able to provide you with comprehensive medical research assistance."""
            
            return ResearchResponse(
                answer=answer,
                sources=[],
                confidence=0.0
            )
        
        # Generate response using Ollama
        ai_response = await ollama_client.generate_response(
            prompt=request.query,
            context=request.context,
            conversation_history=request.conversation_history
        )
        
        # Create mock sources for demonstration
        # In a real implementation, this would come from a vector database
        sources = []
        if "medical" in request.query.lower() or "treatment" in request.query.lower():
            sources = [
                {
                    "title": "Recent Advances in Medical Research",
                    "authors": ["Dr. Smith", "Dr. Johnson"],
                    "journal": "New England Journal of Medicine",
                    "year": 2024,
                    "abstract": "This study discusses recent developments in medical treatments and patient care.",
                    "relevanceScore": 0.92
                },
                {
                    "title": "Clinical Guidelines and Best Practices",
                    "authors": ["Medical Research Team"],
                    "journal": "Journal of Clinical Medicine",
                    "year": 2024,
                    "abstract": "Comprehensive guidelines for medical practitioners based on latest research.",
                    "relevanceScore": 0.88
                }
            ]
        
        # Calculate confidence based on response quality
        confidence = 0.85 if len(ai_response) > 100 else 0.75
        
        return ResearchResponse(
            answer=ai_response,
            sources=sources,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ollama/models")
async def get_models():
    """Get available Ollama models"""
    try:
        models = await ollama_client.get_available_models()
        return {
            "available_models": models,
            "current_model": ollama_client.model,
            "connected": await ollama_client.check_connection()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ollama/model/{model_name}")
async def set_model(model_name: str):
    """Set the Ollama model to use"""
    try:
        success = await ollama_client.set_model(model_name)
        if success:
            return {
                "message": f"Model set to {model_name}",
                "current_model": ollama_client.model
            }
        else:
            raise HTTPException(status_code=400, detail=f"Model {model_name} not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
