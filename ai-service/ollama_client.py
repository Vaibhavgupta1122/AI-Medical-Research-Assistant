import httpx
import json
import asyncio
from typing import Dict, Any, List

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "mistral"  # Default model, can be changed
        
    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False
    
    async def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags", timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    return [model["name"] for model in data.get("models", [])]
                return []
        except Exception:
            return []
    
    async def generate_response(
        self, 
        prompt: str, 
        context: Dict[str, Any] = None,
        conversation_history: List[Dict[str, Any]] = None
    ) -> str:
        """Generate response using Ollama"""
        try:
            # Build the conversation context
            messages = []
            
            # Add system prompt for medical context
            system_prompt = """You are a helpful AI medical research assistant. 
            Provide accurate, evidence-based information about medical topics.
            Always include disclaimers that your information is not a substitute for professional medical advice.
            Be thorough, compassionate, and cite sources when possible."""
            
            messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Last 5 messages to avoid context overflow
                    role = "user" if msg.get("type") == "user" else "assistant"
                    content = msg.get("content", {}).get("text", "")
                    if content:
                        messages.append({"role": role, "content": content})
            
            # Add current user query
            messages.append({"role": "user", "content": prompt})
            
            # Add context information if provided
            if context:
                context_info = "\n\nAdditional Context:\n"
                if context.get("location"):
                    context_info += f"Location: {context['location']}\n"
                if context.get("primaryCondition"):
                    context_info += f"Primary Condition: {context['primaryCondition']}\n"
                if context.get("preferences"):
                    context_info += f"Preferences: {context['preferences']}\n"
                
                if len(context_info) > 20:  # Only add if there's actual context
                    messages.append({"role": "system", "content": context_info})
            
            # Make the API call to Ollama
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 1000
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("message", {}).get("content", "")
                else:
                    raise Exception(f"Ollama API error: {response.status_code}")
                    
        except Exception as e:
            print(f"Error generating response with Ollama: {e}")
            return f"I apologize, but I'm having trouble connecting to the AI service. Error: {str(e)}"
    
    async def set_model(self, model_name: str) -> bool:
        """Change the model being used"""
        try:
            # Check if model is available
            available_models = await self.get_available_models()
            if model_name in available_models:
                self.model = model_name
                return True
            return False
        except Exception:
            return False

# Global Ollama client instance
ollama_client = OllamaClient()
