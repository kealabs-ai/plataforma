import streamlit as st
import requests
import os
import json
from typing import Dict, Any, Optional

def get_api_url():
    """Obtém a URL da API a partir das variáveis de ambiente"""
    return os.getenv("API_URL", "http://localhost:8000")

def trigger_workflow(workflow_id: str, data: Dict[str, Any], token: str) -> Optional[Dict[str, Any]]:
    """
    Aciona um workflow no n8n através da API
    
    Args:
        workflow_id: ID do workflow no n8n
        data: Dados a serem enviados para o workflow
        token: Token de autenticação
        
    Returns:
        Resposta do workflow ou None em caso de erro
    """
    try:
        api_url = get_api_url()
        url = f"{api_url}/workflows/{workflow_id}/trigger"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao acionar workflow: {str(e)}")
        return None

def get_workflow_status(execution_id: str, token: str) -> Optional[Dict[str, Any]]:
    """
    Obtém o status de execução de um workflow
    
    Args:
        execution_id: ID da execução do workflow
        token: Token de autenticação
        
    Returns:
        Status da execução ou None em caso de erro
    """
    try:
        api_url = get_api_url()
        url = f"{api_url}/workflows/execution/{execution_id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao obter status do workflow: {str(e)}")
        return None

def workflow_page():
    """Página de gerenciamento de workflows"""
    st.title("Gerenciamento de Workflows")
    
    # Verifica se o usuário está autenticado
    if "token" not in st.session_state:
        st.warning("Você precisa fazer login para acessar esta página.")
        return
    
    token = st.session_state.token
    
    # Lista de workflows disponíveis (em uma aplicação real, isso viria da API)
    workflows = [
        {"id": "workflow1", "name": "Processamento de Dados"},
        {"id": "workflow2", "name": "Análise de Sentimentos"},
        {"id": "workflow3", "name": "Extração de Entidades"}
    ]
    
    # Seleção de workflow
    selected_workflow = st.selectbox(
        "Selecione um workflow",
        options=[w["id"] for w in workflows],
        format_func=lambda x: next((w["name"] for w in workflows if w["id"] == x), x)
    )
    
    # Área para entrada de dados
    st.subheader("Dados de entrada")
    data_input = st.text_area("JSON de entrada", "{}")
    
    # Botão para acionar o workflow
    if st.button("Executar Workflow"):
        try:
            data = json.loads(data_input)
            with st.spinner("Executando workflow..."):
                result = trigger_workflow(selected_workflow, data, token)
                if result:
                    st.success("Workflow acionado com sucesso!")
                    st.json(result)
                    
                    # Salva o ID da execução para consulta posterior
                    if "execution_id" in result:
                        st.session_state.last_execution_id = result["execution_id"]
        except json.JSONDecodeError:
            st.error("JSON inválido. Verifique o formato dos dados.")
    
    # Área para verificar status de execuções anteriores
    st.subheader("Verificar status de execução")
    execution_id = st.text_input("ID da execução", 
                                value=st.session_state.get("last_execution_id", ""))
    
    if st.button("Verificar Status") and execution_id:
        with st.spinner("Obtendo status..."):
            status = get_workflow_status(execution_id, token)
            if status:
                st.success("Status obtido com sucesso!")
                st.json(status)