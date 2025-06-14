from typing import Dict, Any, Optional
from .base_agent import BaseAgent
from .data_analysis_agent import DataAnalysisAgent

class AgentFactory:
    """Fábrica para criar instâncias de agentes."""
    
    _agents = {
        "data_analysis": DataAnalysisAgent
    }
    
    @classmethod
    def register_agent(cls, name: str, agent_class):
        """
        Registra um novo tipo de agente.
        
        Args:
            name: Nome do agente.
            agent_class: Classe do agente.
        """
        cls._agents[name] = agent_class
    
    @classmethod
    def get_agent(cls, agent_name: str, **kwargs) -> BaseAgent:
        """
        Cria e retorna uma instância do agente especificado.
        
        Args:
            agent_name: Nome do agente.
            **kwargs: Parâmetros adicionais para o construtor do agente.
            
        Returns:
            BaseAgent: Uma instância do agente solicitado.
            
        Raises:
            ValueError: Se o agente especificado não for suportado.
        """
        agent_name = agent_name.lower()
        
        if agent_name in cls._agents:
            return cls._agents[agent_name](**kwargs)
        else:
            raise ValueError(f"Agente não suportado: {agent_name}")
    
    @classmethod
    def list_agents(cls) -> Dict[str, str]:
        """
        Lista todos os agentes disponíveis.
        
        Returns:
            Dict[str, str]: Dicionário com nomes e descrições dos agentes.
        """
        result = {}
        for name, agent_class in cls._agents.items():
            # Cria uma instância temporária para obter a descrição
            agent = agent_class()
            result[name] = agent.description
        return result