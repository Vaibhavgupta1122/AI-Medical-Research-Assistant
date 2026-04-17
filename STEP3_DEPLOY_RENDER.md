# 🚀 STEP 3: DEPLOY BACKEND TO RENDER (FREE)

## Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up/login with GitHub
3. Allow Render access to your repositories

## Deploy Backend Service
1. Click **"New +"**
2. Select **"Web Service"**
3. **Connect Repository**: Choose `ai-medical-research-assistant`
4. **Name**: `ai-medical-research-backend`
5. **Root Directory**: `server`
6. **Runtime**: Node (auto-detected)
7. **Build Command**: `npm install && npm start`
8. **Start Command**: `npm start`
9. **Instance Type**: Free (Free tier)
10. **Environment Variables**:
    ```
    NODE_ENV=production
    MONGODB_URI=mongodb+srv://vaibhavgupta1122:YOUR_NEW_PASSWORD@medical-ai-clusters.710towk.mongodb.net/?appName=medical-ai-clusters
    AI_SERVICE_URL=https://your-ai-service-name.onrender.com
    JWT_SECRET=your-random-secret-key-here
    PORT=5000
    ```
11. Click **"Create Web Service"**

## Wait for Deployment
- Takes 5-10 minutes
- You'll get a URL like: `https://ai-medical-research-backend.onrender.com`
- Check deployment logs in Render dashboard

## Test Backend
1. Visit your Render URL + `/api/health`
2. Should see: `{"status": "healthy", "message": "Backend running"}`
3. Test authentication endpoints

## Next Step
Once backend is deployed, update frontend environment variable and deploy AI service.
