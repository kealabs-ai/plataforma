import os
import requests
import json
from typing import Dict, Any, Optional

class N8NWorkflowManager:
    """
    Classe para gerenciar workflows no n8n
    """
    def __init__(self):
        self.n8n_url = os.getenv("N8N_URL", "http://n8n:5678")
        self.api_key = os.getenv("N8N_API_KEY", "")
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            self.headers["X-N8N-API-KEY"] = self.api_key

    def trigger_workflow(self, workflow_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Aciona um workflow no n8n
        
        Args:
            workflow_id: ID do workflow no n8n
            data: Dados a serem enviados para o workflow
            
        Returns:
            Resposta do workflow ou None em caso de erro
        """
        try:
            url = f"{self.n8n_url}/webhook/{workflow_id}"
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao acionar workflow {workflow_id}: {str(e)}")
            return None

    def get_workflow_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém o status de execução de um workflow
        
        Args:
            execution_id: ID da execução do workflow
            
        Returns:
            Status da execução ou None em caso de erro
        """
        try:
            url = f"{self.n8n_url}/api/v1/executions/{execution_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Erro ao obter status do workflow {execution_id}: {str(e)}")
            return None