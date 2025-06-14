from typing import Dict, Any, Optional
from .base_llm import BaseLLM
from .openai_llm import OpenAILLM
from .gemini_llm import GeminiLLM

class LLMFactory:
    """Fábrica para criar instâncias de LLMs."""
    
    @staticmethod
    def get_llm(model_name: str, **kwargs) -> BaseLLM:
        """
        Cria e retorna uma instância do LLM especificado.
        
        Args:
            model_name: Nome do modelo ou provedor de LLM.
            **kwargs: Parâmetros adicionais para o construtor do LLM.
            
        Returns:
            BaseLLM: Uma instância do LLM solicitado.
            
        Raises:
            ValueError: Se o modelo especificado não for suportado.
        """
        model_name = model_name.lower()
        
        if "openai" in model_name or "gpt" in model_name:
            return OpenAILLM(**kwargs)
        elif "gemini" in model_name or "google" in model_name:
            return GeminiLLM(**kwargs)
        elif "claude" in model_name or "anthropic" in model_name:
            # Implementação para Claude seria adicionada aqui
            from .claude_llm import ClaudeLLM
            return ClaudeLLM(**kwargs)
        elif "llama" in model_name:
            # Implementação para Llama seria adicionada aqui
            from .llama_llm import LlamaLLM
            return LlamaLLM(**kwargs)
        elif "grok" in model_name:
            # Implementação para Grok seria adicionada aqui
            from .grok_llm import GrokLLM
            return GrokLLM(**kwargs)
        else:
            # Fallback para OpenAI se o modelo não for reconhecido
            return OpenAILLM(**kwargs)