# 🚀 FREE DEPLOYMENT GUIDE

## Step 1: Deploy Frontend to Vercel (FREE)

### Prerequisites
- GitHub account
- Vercel account (free)

### Steps
1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-medical-research-assistant.git
git push -u origin main
```

2. **Deploy to Vercel**
- Go to [vercel.com](https://vercel.com)
- Click "New Project"
- Import your GitHub repository
- Select `client` folder as Root Directory
- Set Environment Variables:
  - `REACT_APP_API_URL`: `https://your-backend.onrender.com`
- Click Deploy

## Step 2: Deploy Backend to Render (FREE)

### Prerequisites
- Render account (free tier)

### Steps
1. **Prepare Backend**
```bash
# In server folder
npm install --production
```

2. **Deploy to Render**
- Go to [render.com](https://render.com)
- Click "New +"
- Select "Web Service"
- Connect GitHub repository
- Build Command: `npm install && npm start`
- Start Command: `npm start`
- Environment Variables:
  - `NODE_ENV`: `production`
  - `MONGODB_URI`: Your MongoDB Atlas string
  - `AI_SERVICE_URL`: `https://your-ai-service.onrender.com`
  - `JWT_SECRET`: Generate random secret

## Step 3: Deploy AI Service to Render (FREE)

### Steps
1. **Prepare AI Service**
```bash
# In ai-service folder
pip install -r requirements.txt
```

2. **Deploy to Render**
- Go to [render.com](https://render.com)
- Click "New +"
- Select "Web Service"
- Connect GitHub repository
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  - `OLLAMA_BASE_URL`: `http://localhost:11434` (or your Ollama server)
  - `CHROMA_PERSIST_DIRECTORY`: `./chroma_db`
  - `PUBMED_API_KEY`: Your PubMed key (optional)

## Step 4: Update Environment Variables

### Frontend (.env)
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

### Backend (.env)
```
NODE_ENV=production
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/db
AI_SERVICE_URL=https://your-ai-service.onrender.com
JWT_SECRET=your-secret-key
```

### AI Service (.env)
```
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 🎯 QUICK DEPLOYMENT URLS

After deployment:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.onrender.com`
- **AI Service**: `https://your-ai-service.onrender.com`

## 📝 NOTES

1. **MongoDB Atlas**: Use free tier (512MB)
2. **Render**: Free tier includes 750 hours/month
3. **Vercel**: Free tier with unlimited deployments
4. **Ollama**: Run locally or on separate server

## 🔧 ALTERNATIVE: GitHub Pages (Frontend Only)

If Vercel has issues:
```bash
# Build for GitHub Pages
cd client
npm run build
cp build/index.html build/404.html
```

Deploy to GitHub Pages in repository settings.
