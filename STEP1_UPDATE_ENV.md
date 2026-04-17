# 🔐 STEP 1: UPDATE LOCAL ENVIRONMENT

## Update Server .env File
Replace your MongoDB URI with your NEW password:
```
MONGODB_URI=mongodb+srv://vaibhavgupta1122:YOUR_NEW_PASSWORD@medical-ai-clusters.710towk.mongodb.net/?appName=medical-ai-clusters
PORT=5000
AI_SERVICE_URL=http://localhost:8000
NODE_ENV=development
JWT_SECRET=your-random-secret-key-here
```

## Update AI Service .env File
```
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_PERSIST_DIRECTORY=./chroma_db
PUBMED_API_KEY=your-pubmed-api-key
OPENALEX_API_URL=https://api.openalex.org
CLINICAL_TRIALS_API_URL=https://clinicaltrials.gov/api/query
```

## Update Client .env File
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENV=development
```

## Test Locally
```bash
# Test server
cd server
npm start

# Test AI service
cd ai-service
py -3.12 -m uvicorn simple_main:app --port 8000

# Test frontend
cd client
npm start
```

Once everything works locally, proceed to deployment.
