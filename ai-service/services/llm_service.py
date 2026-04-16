import requests
import json
from typing import List, Dict, Any, Optional
import logging
import time
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class OllamaLLMService:
    def __init__(self, base_url: str = None, model: str = "mistral"):
        """
        Initialize Ollama LLM service
        
        Args:
            base_url: Ollama API base URL
            model: Model to use (mistral, llama3, etc.)
        """
        self.base_url = base_url or os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = model
        self.timeout = 120  # 2 minute timeout
        
        # Test connection
        self.test_connection()
    
    def test_connection(self):
        """Test connection to Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model.get('name', '') for model in models]
                
                if self.model not in model_names:
                    logger.warning(f"Model {self.model} not found. Available models: {model_names}")
                    logger.info(f"Please run: ollama pull {self.model}")
                else:
                    logger.info(f"Connected to Ollama with model {self.model}")
            else:
                logger.error("Failed to connect to Ollama")
        except Exception as e:
            logger.error(f"Ollama connection test failed: {str(e)}")
    
    def generate_response(self, prompt: str, system_prompt: str = None, 
                         temperature: float = 0.7, max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Generate response from Ollama
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response dictionary with text and metadata
        """
        try:
            # Build messages
            messages = []
            
            if system_prompt:
                messages.append({
                    'role': 'system',
                    'content': system_prompt
                })
            
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Prepare request payload
            payload = {
                'model': self.model,
                'messages': messages,
                'stream': False,
                'options': {
                    'temperature': temperature,
                    'num_predict': max_tokens,
                    'top_p': 0.9,
                    'top_k': 40
                }
            }
            
            start_time = time.time()
            
            # Make request to Ollama
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            processing_time = time.time() - start_time
            
            # Parse response
            result = response.json()
            message = result.get('message', {})
            response_text = message.get('content', '')
            
            # Extract usage info if available
            usage = result.get('usage', {})
            tokens_used = usage.get('total_tokens', 0)
            
            return {
                'text': response_text,
                'model': self.model,
                'processing_time': processing_time,
                'tokens_used': tokens_used,
                'temperature': temperature,
                'success': True,
                'raw_response': result
            }
            
        except requests.exceptions.Timeout:
            logger.error(f"LLM request timed out after {self.timeout} seconds")
            return {
                'text': 'I apologize, but the request timed out. Please try again.',
                'model': self.model,
                'error': 'timeout',
                'success': False
            }
        
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to Ollama. Is it running?")
            return {
                'text': 'I apologize, but I\'m currently unable to connect to the AI service. Please ensure Ollama is running.',
                'model': self.model,
                'error': 'connection_error',
                'success': False
            }
        
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return {
                'text': 'I apologize, but an error occurred while generating the response.',
                'model': self.model,
                'error': str(e),
                'success': False
            }
    
    def generate_research_answer(self, query: str, context: List[Dict[str, Any]], 
                              conversation_history: List[Dict[str, Any]] = None,
                              user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate research answer using RAG
        
        Args:
            query: User query
            context: Retrieved documents (publications and trials)
            conversation_history: Previous conversation
            user_context: User demographic/context info
            
        Returns:
            Generated answer with metadata
        """
        try:
            # Import here to avoid circular imports
            from .rag_prompting import create_research_prompt
            
            # Create research prompt
            prompt_data = create_research_prompt(
                query=query,
                context=context,
                conversation_history=conversation_history,
                user_context=user_context
            )
            
            # Generate response
            response = self.generate_response(
                prompt=prompt_data['prompt'],
                system_prompt=prompt_data['system_prompt'],
                temperature=0.3,  # Lower temperature for factual responses
                max_tokens=3000
            )
            
            # Add confidence score based on context quality
            confidence = self.calculate_confidence_score(context, response)
            
            # Extract sources
            sources = self.extract_sources(context)
            
            return {
                'answer': response['text'],
                'model': response['model'],
                'processing_time': response.get('processing_time', 0),
                'tokens_used': response.get('tokens_used', 0),
                'confidence': confidence,
                'sources': sources,
                'context_count': len(context),
                'success': response.get('success', False),
                'error': response.get('error')
            }
            
        except Exception as e:
            logger.error(f"Error generating research answer: {str(e)}")
            return {
                'answer': 'I apologize, but I encountered an error while generating your research answer.',
                'error': str(e),
                'success': False
            }
    
    def calculate_confidence_score(self, context: List[Dict[str, Any]], 
                                 response: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on context quality and response
        
        Args:
            context: Retrieved documents
            response: LLM response
            
        Returns:
            Confidence score (0-1)
        """
        base_confidence = 0.5
        
        # Factor 1: Number of relevant documents
        doc_count = len(context)
        if doc_count >= 10:
            base_confidence += 0.2
        elif doc_count >= 5:
            base_confidence += 0.1
        elif doc_count >= 2:
            base_confidence += 0.05
        
        # Factor 2: Source quality
        pubmed_count = sum(1 for doc in context if doc.get('source') == 'pubmed')
        if pubmed_count >= 5:
            base_confidence += 0.15
        elif pubmed_count >= 2:
            base_confidence += 0.1
        
        # Factor 3: Recency of sources
        current_year = datetime.now().year
        recent_docs = sum(1 for doc in context 
                         if doc.get('year', 0) >= current_year - 5)
        if recent_docs >= len(context) * 0.5:
            base_confidence += 0.1
        
        # Factor 4: Response success
        if response.get('success', False):
            base_confidence += 0.1
        
        # Cap at 1.0
        return min(base_confidence, 1.0)
    
    def extract_sources(self, context: List[Dict[str, Any]]) -> List[str]:
        """Extract unique sources from context"""
        sources = set()
        for doc in context:
            source = doc.get('source', 'unknown')
            sources.add(source)
        return list(sources)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        try:
            response = requests.get(f"{self.base_url}/api/show", 
                                  json={'name': self.model}, 
                                  timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': 'Model not found'}
        except Exception as e:
            return {'error': str(e)}
    
    def list_models(self) -> List[str]:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [model.get('name', '') for model in models]
            else:
                return []
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return []

# Global LLM service instance
llm_service = OllamaLLMService()

def generate_research_answer(query: str, context: List[Dict[str, Any]], 
                          conversation_history: List[Dict[str, Any]] = None,
                          user_context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Convenience function to generate research answer
    
    Args:
        query: User query
        context: Retrieved documents
        conversation_history: Previous conversation
        user_context: User context
        
    Returns:
        Generated answer with metadata
    """
    return llm_service.generate_research_answer(
        query=query,
        context=context,
        conversation_history=conversation_history,
        user_context=user_context
    )

# Test function
def test_llm_service():
    """Test the LLM service"""
    print("Testing LLM service...")
    
    # Test connection
    models = llm_service.list_models()
    print(f"Available models: {models}")
    
    # Test simple generation
    test_prompt = "What is Parkinson disease?"
    response = llm_service.generate_response(test_prompt)
    
    print(f"Test response:")
    print(f"Model: {response.get('model', 'unknown')}")
    print(f"Success: {response.get('success', False)}")
    print(f"Response: {response.get('text', 'No response')[:200]}...")
    print(f"Processing time: {response.get('processing_time', 0):.2f}s")
    
    # Test research answer generation
    test_context = [
        {
            'title': 'Deep Brain Stimulation for Parkinson Disease',
            'abstract': 'A clinical trial examining DBS effectiveness.',
            'source': 'pubmed',
            'year': 2023,
            'authors': ['Dr. Smith'],
            'journal': 'Neurology'
        }
    ]
    
    research_response = generate_research_answer(
        query="What are the latest treatments for Parkinson disease?",
        context=test_context
    )
    
    print(f"\nResearch answer test:")
    print(f"Success: {research_response.get('success', False)}")
    print(f"Confidence: {research_response.get('confidence', 0):.2f}")
    print(f"Answer: {research_response.get('answer', 'No answer')[:300]}...")

if __name__ == "__main__":
    test_llm_service()
