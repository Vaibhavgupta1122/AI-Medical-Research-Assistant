#!/usr/bin/env python3
"""
AI Medical Research Service Startup Script with Ollama Integration
"""
import asyncio
import subprocess
import sys
import time
from ollama_client import ollama_client

async def check_ollama():
    """Check if Ollama is running and configured"""
    print("Checking Ollama connection...")
    
    # Check if Ollama is running
    if not await ollama_client.check_connection():
        print("Ollama is not running. Please start Ollama first:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Start Ollama: ollama serve")
        print("3. Pull Mistral model: ollama pull mistral")
        return False
    
    print("Ollama is connected!")
    
    # Check available models
    models = await ollama_client.get_available_models()
    print(f"Available models: {models}")
    
    if "mistral" not in models:
        print("Mistral model not found. Pulling it now...")
        try:
            subprocess.run(["ollama", "pull", "mistral"], check=True)
            print("Mistral model pulled successfully!")
        except subprocess.CalledProcessError:
            print("Failed to pull Mistral model. Please run: ollama pull mistral")
            return False
    
    return True

async def start_ai_service():
    """Start the AI service"""
    print("\nStarting AI Medical Research Service...")
    print("Service will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    
    # Import and run the FastAPI app
    import uvicorn
    from simple_main import app
    
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Main startup function"""
    print("=" * 60)
    print("AI Medical Research Service with Ollama")
    print("=" * 60)
    
    # Check Ollama setup
    if not await check_ollama():
        print("\nPlease fix the Ollama setup and try again.")
        sys.exit(1)
    
    print("\nAll checks passed! Starting AI service...")
    
    try:
        await start_ai_service()
    except KeyboardInterrupt:
        print("\nShutting down AI service...")
    except Exception as e:
        print(f"Error starting AI service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
