from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional, Dict, Any
import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz ao path para importações relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa módulos do backend
from backend.database import get_db, Database
from backend.models import UserCreate, User, LLMRequest, LLMResponse
from backend.auth import create_access_token, get_current_user
from workflows import N8NWorkflowManager

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Kognia One API",
    description="API para a plataforma Kognia One",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Inicializa o gerenciador de workflows n8n
workflow_manager = N8NWorkflowManager()

# Rotas de autenticação
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()
    user = db.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Rotas de usuários
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    db = get_db()
    db_user = db.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já registrado")
    return db.create_user(user)

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Rotas para LLMs
@app.post("/llm/generate", response_model=LLMResponse)
async def generate_llm_response(
    request: LLMRequest,
    current_user: User = Depends(get_current_user)
):
    from llms.llm_factory import LLMFactory
    
    try:
        llm = LLMFactory.get_llm(request.model)
        response = llm.generate(request.prompt)
        return {"response": response, "model": request.model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rotas para agentes
@app.post("/agents/run")
async def run_agent(
    agent_name: str,
    params: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    from agents.agent_factory import AgentFactory
    
    try:
        agent = AgentFactory.get_agent(agent_name)
        result = agent.run(params)
        return {"result": result, "agent": agent_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rotas para workflows n8n
@app.post("/workflows/{workflow_id}/trigger")
async def trigger_workflow(
    workflow_id: str,
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    Aciona um workflow no n8n
    """
    result = workflow_manager.trigger_workflow(workflow_id, data)
    if not result:
        raise HTTPException(status_code=500, detail="Erro ao acionar workflow")
    return result

@app.get("/workflows/execution/{execution_id}")
async def get_workflow_status(
    execution_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Obtém o status de execução de um workflow
    """
    result = workflow_manager.get_workflow_status(execution_id)
    if not result:
        raise HTTPException(status_code=404, detail="Execução não encontrada")
    return result

# Rota de status
@app.get("/status")
async def get_status():
    return {"status": "online", "version": "1.0.0"}

# Inicialização da aplicação
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    # Para execução local, use a string de importação
    if os.getenv("DOCKER_ENV") == "true":
        # No Docker, use o objeto app diretamente
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # Fora do Docker, use a string de importação para habilitar o reload
        uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)