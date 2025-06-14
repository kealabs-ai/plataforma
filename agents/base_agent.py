from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAgent(ABC):
    """Classe base para todos os agentes inteligentes."""
    
    def __init__(self, **kwargs):
        self.config = kwargs
    
    @abstractmethod
    def run(self, params: Dict[str, Any]) -> Any:
        """
        Executa o agente com os parâmetros fornecidos.
        
        Args:
            params: Parâmetros para a execução do agente.
            
        Returns:
            Any: O resultado da execução do agente.
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Retorna o nome do agente.
        
        Returns:
            str: Nome do agente.
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """
        Retorna a descrição do agente.
        
        Returns:
            str: Descrição do agente.
        """
        pass