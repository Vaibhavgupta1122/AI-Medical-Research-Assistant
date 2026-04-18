# # Ollama Integration Guide

## **OLLAMA SETUP FOR AI MEDICAL RESEARCH ASSISTANT**

### **Step 1: Install Ollama**

#### **Windows:**
1. Download Ollama from: https://ollama.ai/
2. Run the installer
3. Restart your terminal/command prompt

#### **Verify Installation:**
```bash
ollama --version
```

### **Step 2: Start Ollama Service**

#### **Option 1: Start Manually**
```bash
ollama serve
```

#### **Option 2: Start as Background Service**
```bash
# Windows
start "Ollama" ollama serve

# Linux/Mac
ollama serve &
```

#### **Verify Ollama is Running:**
```bash
curl http://localhost:11434/api/tags
```

### **Step 3: Download AI Model**

#### **Pull Mistral Model (Recommended):**
```bash
ollama pull mistral
```

#### **Other Available Models:**
```bash
ollama pull llama2
ollama pull codellama
ollama pull vicuna
```

#### **Verify Models:**
```bash
ollama list
```

### **Step 4: Start AI Service**

#### **Automatic Start (Recommended):**
```bash
cd ai-service
.\START_OLLAMA.bat
```

#### **Manual Start:**
```bash
cd ai-service
py -3.12 -m uvicorn simple_main:app --host 0.0.0.0 --port 8000
```

### **Step 5: Verify Integration**

#### **Check AI Service Health:**
```bash
curl http://localhost:8000/health
```

#### **Expected Response:**
```json
{
  "status": "healthy",
  "service": "AI Medical Research Service",
  "ollama": {
    "connected": true,
    "available_models": ["mistral"],
    "current_model": "mistral"
  }
}
```

#### **Check Available Models:**
```bash
curl http://localhost:8000/ollama/models
```

### **Step 6: Test AI Integration**

#### **Send Test Query:**
```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest treatments for diabetes?"}'
```

---

## **TROUBLESHOOTING**

### **Common Issues:**

#### **1. Ollama Not Found**
```bash
# Error: 'ollama' is not recognized
# Solution: Add Ollama to PATH or restart terminal
```

#### **2. Connection Refused**
```bash
# Error: curl: (7) Failed to connect to localhost port 11434
# Solution: Start Ollama service: ollama serve
```

#### **3. Model Not Found**
```bash
# Error: model 'mistral' not found
# Solution: Pull the model: ollama pull mistral
```

#### **4. AI Service Fails**
```bash
# Error: Cannot connect to Ollama
# Solution: Ensure Ollama is running before starting AI service
```

### **Debug Commands:**

#### **Check Ollama Status:**
```bash
# Check if Ollama is running
netstat -ano | findstr :11434

# Check available models
ollama list

# Test Ollama directly
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Hello, how are you?",
  "stream": false
}'
```

#### **Check AI Service Logs:**
```bash
# Look for connection errors in AI service output
# Check if Ollama endpoint is reachable
```

---

## **ADVANCED CONFIGURATION**

### **Change AI Model:**
```bash
# Pull a different model
ollama pull llama2

# Set model via API
curl -X POST http://localhost:8000/ollama/model/llama2

# Or modify ollama_client.py to change default
```

### **Model Parameters:**
```python
# In ollama_client.py, modify the options:
"options": {
    "temperature": 0.7,      # Creativity (0.0-1.0)
    "top_p": 0.9,           # Nucleus sampling (0.0-1.0)
    "max_tokens": 1000,     # Response length
    "seed": 42              # Reproducibility
}
```

### **Custom System Prompt:**
```python
# In ollama_client.py, modify the system_prompt variable
system_prompt = """You are a helpful AI medical research assistant..."""
```

---

## **PERFORMANCE TIPS**

### **Optimize Ollama:**
```bash
# Set environment variables for better performance
set OLLAMA_HOST=localhost:11434
set OLLAMA_NUM_PARALLEL=4
```

### **AI Service Optimization:**
```python
# Adjust timeout in ollama_client.py
timeout=60.0  # Increase for longer responses
```

---

## **SUCCESS INDICATORS**

### **Working Setup Should Show:**
- [x] Ollama service running on port 11434
- [x] Mistral model downloaded and available
- [x] AI service running on port 8000
- [x] Health check shows Ollama connected: true
- [x] Research queries return AI-generated responses
- [x] Frontend can send and receive messages

### **Test the Full Flow:**
1. Start all services (backend, AI with Ollama, frontend)
2. Open http://localhost:3000
3. Send a message like "What is diabetes?"
4. Should receive AI-generated response from Mistral

---

**Your AI Medical Research Assistant is now powered by Ollama!**
