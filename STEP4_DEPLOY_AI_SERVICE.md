# 🤖 STEP 4: DEPLOY AI SERVICE TO RENDER (FREE)

## Deploy AI Service
1. Go to [render.com](https://render.com) (already logged in)
2. Click **"New +"**
3. Select **"Web Service"**
4. **Connect Repository**: Choose `ai-medical-research-assistant`
5. **Name**: `ai-medical-research-service`
6. **Root Directory**: `ai-service`
7. **Runtime**: Python (auto-detected)
8. **Build Command**: `pip install -r requirements.txt`
9. **Start Command**: `uvicorn simple_main:app --host 0.0.0.0 --port $PORT`
10. **Instance Type**: Free (Free tier)
11. **Environment Variables**:
    ```
    OLLAMA_BASE_URL=http://localhost:11434
    CHROMA_PERSIST_DIRECTORY=./chroma_db
    PUBMED_API_KEY=your-pubmed-api-key
    OPENALEX_API_URL=https://api.openalex.org
    CLINICAL_TRIALS_API_URL=https://clinicaltrials.gov/api/query
    ```
12. Click **"Create Web Service"**

## Wait for Deployment
- Takes 5-10 minutes
- You'll get a URL like: `https://ai-medical-research-service.onrender.com`
- Check deployment logs in Render dashboard

## Test AI Service
1. Visit your Render URL + `/health`
2. Should see: `{"status": "healthy", "service": "AI Medical Research Service"}`
3. Test research endpoint with curl or Postman

## Step 5: Connect Services
Update backend environment variable:
- `AI_SERVICE_URL`: `https://ai-medical-research-service.onrender.com`
- Redeploy backend from Render dashboard

## Final Step: Update Frontend
Update Vercel environment:
- `REACT_APP_API_URL`: `https://ai-medical-research-backend.onrender.com`
- Redeploy from Vercel dashboard

## 🎯 FINAL URLS
- **Frontend**: `https://ai-medical-research-assistant.vercel.app`
- **Backend**: `https://ai-medical-research-backend.onrender.com`
- **AI Service**: `https://ai-medical-research-service.onrender.com`
