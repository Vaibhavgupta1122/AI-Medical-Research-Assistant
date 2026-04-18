# 🚀 AI Medical Research Assistant - Complete Startup Guide

## 🎯 **EASIEST WAY - ONE COMMAND**

### **Step 1: Run the Ultimate Fix**
```bash
cd C:\Users\VAIBHAV GUPTA\OneDrive\Documents\GITHUB\AI-Medical-Research-Assistant
.\COMPLETE_TERMINAL_FIX.bat
```

**That's it! Everything will start automatically.**

---

## 📋 **DETAILED STEP-BY-STEP GUIDE**

### **Option 1: Automatic (Recommended)**
1. Open Command Prompt or PowerShell
2. Navigate to project folder:
   ```bash
   cd C:\Users\VAIBHAV GUPTA\OneDrive\Documents\GITHUB\AI-Medical-Research-Assistant
   ```
3. Run the complete fix:
   ```bash
   .\COMPLETE_TERMINAL_FIX.bat
   ```
4. Wait for completion (about 30 seconds)
5. Access your application

### **Option 2: Manual (3 Separate Terminals)**

#### **Terminal 1: Backend Server**
```bash
cd C:\Users\VAIBHAV GUPTA\OneDrive\Documents\GITHUB\AI-Medical-Research-Assistant\server
npm start
```

#### **Terminal 2: AI Service (with Ollama)**
```bash
# First, install and start Ollama:
# 1. Install Ollama: https://ollama.ai/
# 2. Start Ollama: ollama serve
# 3. Pull model: ollama pull mistral

# Then start AI service:
cd C:\Users\VAIBHAV GUPTA\OneDrive\Documents\GITHUB\AI-Medical-Research-Assistant\ai-service
.\START_OLLAMA.bat
```

#### **Terminal 3: Frontend**
```bash
cd C:\Users\VAIBHAV GUPTA\OneDrive\Documents\GITHUB\AI-Medical-Research-Assistant\client
npm start
```

---

## 🌐 **Access Your Application**

### **Main Application**
- **Frontend**: http://localhost:3000
- **Login/Signup**: Available on frontend

### **Service Endpoints**
- **Backend API**: http://localhost:5000/api/*
- **AI Service**: http://localhost:8000/*

### **Health Checks**
- **Backend Health**: http://localhost:5000/api/health
- **AI Service Health**: http://localhost:8000/health

---

## 🎯 **What Each Service Does**

### **Frontend (Port 3000)**
- React web application
- User interface
- Login/Signup forms
- Chat interface

### **Backend Server (Port 5000)**
- Node.js/Express server
- User authentication
- Database operations
- API endpoints

### **AI Service (Port 8000)**
- Python FastAPI service
- Medical research processing
- AI responses
- Research integration

---

## ✅ **Success Indicators**

When everything is working, you'll see:

### **Backend Server**
```
Server running on port 5000
Environment: development
MongoDB Connected: ac-7c7uwxm-shard-00-02.710towk.mongodb.net
Database indexes created successfully
```

### **AI Service**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### **Frontend**
```
Compiled successfully!
You can now view ai-medical-research-client in the browser.
  Local:            http://localhost:3000
```

---

## 🧪 **Testing Everything**

### **1. Test Backend**
```bash
curl http://localhost:5000/api/health
```
Should return: `{"status":"OK",...}`

### **2. Test AI Service**
```bash
curl http://localhost:8000/health
```
Should return: `{"status":"healthy",...}`

### **3. Test Frontend**
- Open browser to: http://localhost:3000
- Should see login/signup page

---

## 🚨 **Troubleshooting**

### **If Something Goes Wrong:**

1. **Stop Everything**: Close all terminals
2. **Run Ultimate Fix**: `.\COMPLETE_TERMINAL_FIX.bat`
3. **Wait**: Let it complete fully
4. **Try Again**: Services should work

### **Common Issues:**

- **Port conflicts**: Use the complete fix
- **Backend not responding**: Wait 10 more seconds
- **AI service errors**: Check Python installation
- **Frontend not loading**: Check Node.js installation

---

## 🎉 **You're Ready!**

After running the complete fix:
1. Open browser to: http://localhost:3000
2. Sign up with any email + name
3. Start using your AI Medical Research Assistant!

---

**🚀 Recommended: Always use `.\COMPLETE_TERMINAL_FIX.bat` for the best experience!**
