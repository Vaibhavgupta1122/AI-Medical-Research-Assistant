# 🚀 STEP 2: DEPLOY FRONTEND TO VERCEL (FREE)

## Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Allow Vercel access to your repositories

## Deploy Frontend
1. Click **"New Project"**
2. Select **"Import Git Repository"**
3. Choose **"ai-medical-research-assistant"** from your GitHub
4. **Root Directory**: Set to `client`
5. **Framework Preset**: React (auto-detected)
6. **Environment Variables**:
   - `REACT_APP_API_URL`: `https://your-backend-name.onrender.com`
7. Click **"Deploy"**

## Wait for Deployment
- Takes 2-3 minutes
- You'll get a URL like: `https://ai-medical-research-assistant.vercel.app`

## Test Frontend
1. Visit your Vercel URL
2. Should see login page
3. Try registering/logging in (will use mock backend)

## Next Step
Once frontend is deployed, proceed to deploy backend to Render.
