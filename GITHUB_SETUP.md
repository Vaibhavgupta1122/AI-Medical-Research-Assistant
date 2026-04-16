# 🚀 GITHUB SETUP & DEPLOYMENT GUIDE

## Step 1: Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name: `ai-medical-research-assistant`
4. Description: `AI-powered medical research assistant with RAG system`
5. Make it Public
6. Click "Create repository"

## Step 2: Push to GitHub
```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-medical-research-assistant.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Vercel (Frontend - FREE)

### Option A: Automatic Deployment
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import from GitHub
4. Select `ai-medical-research-assistant` repository
5. Root Directory: `client`
6. Environment Variables:
   - `REACT_APP_API_URL`: `https://your-backend.onrender.com`
7. Click "Deploy"

### Option B: Manual Deployment
```bash
cd client
npm run build
# Upload build folder to Vercel
```

## Step 4: Deploy to Render (Backend & AI Service - FREE)

### Backend Service
1. Go to [render.com](https://render.com)
2. Click "New +"
3. Select "Web Service"
4. Connect GitHub repository
5. Build Command: `npm install && npm start`
6. Start Command: `npm start`
7. Environment Variables:
   ```
   NODE_ENV=production
   MONGODB_URI=mongodb+srv://vaibhavgupta1122:Vaibhav1212@medical-ai-clusters.710towk.mongodb.net/db
   AI_SERVICE_URL=https://your-ai-service.onrender.com
   JWT_SECRET=your-random-secret-key
   PORT=5000
   ```

### AI Service
1. Another "New +" on Render
2. Select "Web Service"
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Environment Variables:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   CHROMA_PERSIST_DIRECTORY=./chroma_db
   PUBMED_API_KEY=your-pubmed-key
   ```

## Step 5: Update Frontend Environment
After backend deployment, update Vercel environment:
- `REACT_APP_API_URL`: `https://your-backend-service.onrender.com`

## Step 6: Test Deployment
1. Frontend: `https://your-app.vercel.app`
2. Backend Health: `https://your-backend.onrender.com/api/health`
3. AI Service Health: `https://your-ai-service.onrender.com/health`

## 🎯 QUICK DEPLOYMENT URLS
- **Frontend**: `https://ai-medical-research-assistant.vercel.app`
- **Backend**: `https://ai-medical-research-api.onrender.com`
- **AI Service**: `https://ai-medical-research-service.onrender.com`

## 🔧 TROUBLESHOOTING

### MongoDB Connection Issues
1. Whitelist IP in MongoDB Atlas
2. Use correct connection string format
3. Check network access settings

### Build Failures
1. Check package.json scripts
2. Verify environment variables
3. Check build logs

### CORS Issues
1. Update CORS origins
2. Check API URLs
3. Verify environment variables

## 📋 CHECKLIST
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Render
- [ ] AI service deployed to Render
- [ ] Environment variables configured
- [ ] All services tested and working
