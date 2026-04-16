# AI Medical Research Assistant

A production-ready Retrieval Augmented Generation (RAG) system for medical research that retrieves real medical research and reasons over it using a local open-source LLM.

## Architecture

- **Frontend**: React + Tailwind
- **Backend**: Node.js + Express
- **Database**: MongoDB
- **AI Service**: Python FastAPI
- **LLM**: Local model via Ollama (Mistral or Llama3)
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers all-MiniLM-L6-v2

## External APIs

1. PubMed API
2. OpenAlex API
3. ClinicalTrials.gov API

## Quick Start

### Prerequisites

1. Node.js 18+
2. Python 3.9+
3. MongoDB
4. Ollama (for local LLM)

### Setup

```bash
# Clone and install dependencies
git clone <repository>
cd AI-Medical-Research-Assistant

# Frontend
cd client
npm install
npm start

# Backend
cd ../server
npm install
npm run dev

# AI Service
cd ../ai-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Ollama (run once)
ollama pull mistral
# or
ollama pull llama3
```

### Environment Variables

Create `.env` files in each service directory:

**server/.env**:
```
MONGODB_URI=mongodb+srv://your-connection-string
PORT=5000
AI_SERVICE_URL=http://localhost:8000
```

**ai-service/.env**:
```
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## Features

- Structured + natural queries
- Deep research retrieval (50-300 docs before filtering)
- Vector search + reranking
- Multi-turn conversation memory
- Structured evidence-based answers
- Display publications + clinical trials

## Project Structure

```
root/
  client/          # React frontend
  server/          # Node.js API
  ai-service/      # Python FastAPI AI service
```