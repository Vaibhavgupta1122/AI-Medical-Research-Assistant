from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import time
import logging
from datetime import datetime

# Import our AI modules
from services.query_understanding import expand_query
from services.retrieval import retrieve_documents
from services.vector_store import VectorStore
from services.reranking import rerank_documents
from services.llm_service import generate_research_answer
from services.rag_prompting import create_research_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Medical Research Service",
    description="RAG-based medical research assistant",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector store
vector_store = VectorStore()

class QueryRequest(BaseModel):
    message: str
    conversationHistory: List[Dict[str, Any]] = []
    context: Dict[str, Any] = {}
    userId: str

class ResearchResponse(BaseModel):
    answer: str
    research: Dict[str, Any]
    processingTime: float
    tokensUsed: int
    modelUsed: str
    sources: List[str]
    confidence: float

@app.get("/")
async def root():
    return {"message": "AI Medical Research Service is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/research", response_model=ResearchResponse)
async def research_endpoint(request: QueryRequest):
    """
    Main research endpoint that orchestrates the full AI pipeline:
    1. Query understanding and expansion
    2. Document retrieval from multiple sources
    3. Vector search and reranking
    4. LLM generation with RAG
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing research request: {request.message[:100]}...")
        
        # Step 1: Query Understanding
        expanded_query = expand_query(
            disease=request.context.get('primaryCondition', ''),
            user_query=request.message,
            conversation_history=request.conversationHistory
        )
        
        logger.info(f"Expanded query: {expanded_query}")
        
        # Step 2: Document Retrieval
        retrieved_docs = retrieve_documents(
            query=expanded_query,
            disease=request.context.get('primaryCondition', ''),
            location=request.context.get('location', {}),
            max_docs=200
        )
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents")
        
        # Step 3: Vector Search & Reranking
        # First, add documents to vector store if not already there
        vector_store.add_documents(retrieved_docs)
        
        # Get top documents using vector search
        top_k_docs = vector_store.search(expanded_query, k=30)
        
        # Rerank documents
        reranked_docs = rerank_documents(
            query=expanded_query,
            documents=top_k_docs,
            context=request.context
        )
        
        # Extract top publications and trials
        top_publications = reranked_docs[:8]
        top_trials = [doc for doc in reranked_docs[8:13] if doc.get('type') == 'clinical_trial']
        
        # Step 4: Generate Research Answer
        context_docs = top_publications + top_trials
        
        research_answer = generate_research_answer(
            query=request.message,
            context=context_docs,
            conversation_history=request.conversationHistory,
            user_context=request.context
        )
        
        # Prepare response
        processing_time = time.time() - start_time
        
        research_data = {
            "publications": [
                {
                    "id": doc.get('id', ''),
                    "title": doc.get('title', ''),
                    "authors": doc.get('authors', []),
                    "journal": doc.get('journal', ''),
                    "year": doc.get('year', 0),
                    "abstract": doc.get('abstract', ''),
                    "doi": doc.get('doi', ''),
                    "relevanceScore": doc.get('relevance_score', 0.0),
                    "source": doc.get('source', 'unknown')
                } for doc in top_publications if doc.get('type') == 'publication'
            ],
            "clinicalTrials": [
                {
                    "nctId": doc.get('nct_id', ''),
                    "title": doc.get('title', ''),
                    "status": doc.get('status', ''),
                    "phase": doc.get('phase', ''),
                    "conditions": doc.get('conditions', []),
                    "location": doc.get('location', ''),
                    "eligibility": doc.get('eligibility', ''),
                    "contacts": doc.get('contacts', []),
                    "relevanceScore": doc.get('relevance_score', 0.0)
                } for doc in top_trials
            ]
        }
        
        sources = [doc.get('source', 'unknown') for doc in context_docs]
        unique_sources = list(set(sources))
        
        response = ResearchResponse(
            answer=research_answer['answer'],
            research=research_data,
            processingTime=processing_time,
            tokensUsed=research_answer.get('tokens_used', 0),
            modelUsed=research_answer.get('model', 'mistral'),
            sources=unique_sources,
            confidence=research_answer.get('confidence', 0.8)
        )
        
        logger.info(f"Research completed in {processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Research endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Research processing failed: {str(e)}")

@app.post("/test-retrieval")
async def test_retrieval(query: str, disease: str = ""):
    """Test endpoint for document retrieval"""
    try:
        docs = retrieve_documents(query=query, disease=disease, max_docs=20)
        return {"query": query, "documents_found": len(docs), "sample": docs[:3]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test-vector-search")
async def test_vector_search(query: str, k: int = 10):
    """Test endpoint for vector search"""
    try:
        results = vector_store.search(query, k=k)
        return {"query": query, "results": len(results), "sample": results[:3]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
