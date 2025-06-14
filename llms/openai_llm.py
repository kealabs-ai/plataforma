import os
from typing import Dict, Any, Optional, List
import requests
from dotenv import load_dotenv
from .base_llm import BaseLLM

# Carrega variáveis de ambiente
load_dotenv()

class OpenAILLM(BaseLLM):
    """Implementação do LLM usando a API da OpenAI."""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        super().__init__(api_key=api_key, **kwargs)
        self.api_url = "https://api.openai.com/v1"
        self.model = kwargs.get("model", "gpt-4")
        
        if not self.validate_api_key():
            raise ValueError("OpenAI API key não configurada")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Gera uma resposta usando a API da OpenAI.
        
        Args:
            prompt: O texto de entrada para o modelo.
            **kwargs: Parâmetros adicionais para a API.
            
        Returns:
            str: A resposta gerada pelo modelo.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": kwargs.get("model", self.model),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Erro ao gerar resposta: {str(e)}"
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Obtém o embedding vetorial para o texto fornecido usando a API da OpenAI.
        
        Args:
            text: O texto para gerar o embedding.
            
        Returns:
            List[float]: O vetor de embedding.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "text-embedding-ada-002",
            "input": text
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/embeddings",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            print(f"Erro ao gerar embedding: {str(e)}")
            return []