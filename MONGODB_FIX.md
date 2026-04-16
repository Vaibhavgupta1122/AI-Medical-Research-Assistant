# 🔧 MONGODB CONNECTION FIX

## Problem
Your IP address is not whitelisted in MongoDB Atlas cluster.

## Quick Fix (2 minutes)

### Option 1: Whitelist Your IP (Recommended)
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Click on your cluster: `medical-ai-clusters`
3. Go to **Network Access** (left sidebar)
4. Click **Add IP Address**
5. Select **Current IP Address** 
6. Click **Confirm**
7. Wait 2-3 minutes for changes to apply

### Option 2: Allow All IPs (Less Secure)
1. In Network Access, click **Add IP Address**
2. Select **Allow Access from Anywhere** (0.0.0.0/0)
3. Click **Confirm**

### Option 3: Use Local MongoDB (Development Only)
Install MongoDB locally and update `.env`:
```
MONGODB_URI=mongodb://localhost:27017/medical_ai
```

## Test Connection
After fixing IP, run:
```bash
cd server
npm start
```

You should see: "Connected to MongoDB" instead of connection error.
