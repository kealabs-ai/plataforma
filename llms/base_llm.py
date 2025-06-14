from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseLLM(ABC):
    """Classe base para todos os modelos de linguagem."""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Gera uma resposta com base no prompt fornecido.
        
        Args:
            prompt: O texto de entrada para o modelo.
            **kwargs: Parâmetros adicionais específicos do modelo.
            
        Returns:
            str: A resposta gerada pelo modelo.
        """
        pass
    
    @abstractmethod
    def get_embedding(self, text: str) -> list:
        """
        Obtém o embedding vetorial para o texto fornecido.
        
        Args:
            text: O texto para gerar o embedding.
            
        Returns:
            list: O vetor de embedding.
        """
        pass
    
    def validate_api_key(self) -> bool:
        """
        Valida se a chave de API está configurada e é válida.
        
        Returns:
            bool: True se a chave for válida, False caso contrário.
        """
        return self.api_key is not None and len(self.api_key) > 0