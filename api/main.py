from fastapi import FastAPI, Depends, HTTPException, status, File, Form, UploadFile, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional, Dict, Any
from datetime import date
import os
import sys
from dotenv import load_dotenv
from pydantic import ValidationError, BaseModel # Importar BaseModel

import requests
import base64

# Adiciona o diretório raiz ao path para importações relativas
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Importa módulos após adicionar o path
# Certifique-se de que MilkProductionEntry e MilkProductionUpdate estejam definidas
# em um arquivo acessível, ou no próprio main.py se preferir.
# Neste caso, elas já estão no seu código fornecido.
from milk_production import MilkProductionEntry, MilkProductionUpdate, AnimalResponse
from visitor import ChatRequest, ChatResponse

# Importa configurações com fallback
try:
    from config import GOOGLE_GEMINI_API_KEY, API_PORT, DOCKER_ENV
except ImportError:
    GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
    API_PORT = int(os.getenv("API_PORT", 8501))
    DOCKER_ENV = os.getenv("DOCKER_ENV", "false")

# Importa módulos do backend
from backend.database import get_db, Database
from backend.models import UserCreate, User, LLMRequest, LLMResponse
from backend.auth import create_access_token, get_current_user
from workflows import N8NWorkflowManager
from visitor import router as visitor_router
from agro import router as agro_router
from milk_production import router as milk_router
from animals_production import router as animals_production_router
from milk_total import router as milk_total_router
from milk_daily_by_animal import router as milk_daily_by_animal_router

# Importa a instância do banco de dados (certifique-se de que milk_db está acessível)
from backend.milk_database import milk_db # Importa a instância global

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Kognia One API",
    description="API para a plataforma Kognia One",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta arquivos estáticos apenas se os diretórios existirem
static_dir = os.path.join(parent_dir, "frontend", "static")
templates_dir = os.path.join(parent_dir, "frontend", "templates")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
if os.path.exists(templates_dir):
    app.mount("/templates", StaticFiles(directory=templates_dir), name="templates")

# Esquema de autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Inicializa o gerenciador de workflows n8n
workflow_manager = N8NWorkflowManager()

# Inclui os routers (mantidos por organização, mas os novos endpoints abaixo são diretos do app)
app.include_router(visitor_router)
app.include_router(agro_router)
app.include_router(milk_router)
app.include_router(animals_production_router)
app.include_router(milk_total_router)
app.include_router(milk_daily_by_animal_router)

# --- Modelos Pydantic para as Novas Respostas ---
class MonthlyMilkProductionResponse(BaseModel):
    month: str
    total_liters: float

# Rota de compatibilidade para /chat
@app.post("/chat")
async def chat_compatibility(request: dict):
    from visitor import chat
    
    try:
        chat_request = ChatRequest(**request)
        response = await chat(chat_request)
        return {"response": response.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota de compatibilidade para /audio-chat
@app.post("/audio-chat")
async def audio_chat_compatibility(audio: UploadFile = File(...), sector: str = Form("")):
    from visitor import audio_chat
    
    try:
        response = await audio_chat(audio, sector)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rotas para servir arquivos HTML
@app.get("/")
async def serve_index():
    file_path = os.path.join(parent_dir, "frontend", "templates", "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/index.html")
async def serve_index_alt():
    file_path = os.path.join(parent_dir, "frontend", "templates", "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/dash_agro.html")
async def serve_dash_agro():
    file_path = os.path.join(parent_dir, "frontend", "templates", "dash_agro.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/dash_agro")
async def serve_dash_agro_alt():
    file_path = os.path.join(parent_dir, "frontend", "templates", "dash_agro.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/visitor.html")
async def serve_visitor():
    file_path = os.path.join(parent_dir, "frontend", "templates", "visitor.html")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="File not found")

# Mantém a rota de token na raiz para compatibilidade
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

# Rota de status
@app.get("/status")
async def get_status():
    return {"status": "online", "version": "1.0.0", "message": "API is running correctly"}

# Rota para suprimir logs do Chrome DevTools
@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools():
    return {}

# Rotas de proxy para compatibilidade com /api/agro/...
@app.get("/api/agro/dashboard-data")
async def proxy_dashboard_data():
    from agro import get_dashboard_data
    return await get_dashboard_data()

@app.get("/api/agro/productions")
async def proxy_productions():
    from agro import get_productions
    return await get_productions()

@app.get("/api/agro/milk-production")
async def proxy_milk_production():
    from agro import get_milk_production
    return await get_milk_production()

@app.get("/api/agro/inputs")
async def proxy_inputs():
    from agro import get_inputs
    return await get_inputs()

@app.get("/api/agro/soil-analysis")
async def proxy_soil_analysis():
    from agro import get_soil_analysis
    return await get_soil_analysis()

@app.get("/api/agro/finances")
async def proxy_finances():
    from agro import get_finances
    return await get_finances()

# --- Rotas diretas para /api/milk/... ---

@app.get("/api/milk/dashboard")
async def api_milk_dashboard(
    start_date: Optional[date] = Query(None, description="Data de início (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Data de fim (YYYY-MM-DD)"),
    animal_id: Optional[int] = Query(None, description="ID do animal para filtrar")
):
    """Obtém dados para o dashboard de produção de leite."""
    # Obter dados reais do banco de dados
    daily_production = milk_db.get_daily_milk_production(start_date, end_date)
    animal_production = milk_db.get_milk_production_by_animal()
    total_animals = milk_db.count_animals()

    # Calcular estatísticas
    total_liters = sum(item['total_liters'] for item in daily_production)
    milk_price = 2.50  # Preço por litro em R$
    total_value = total_liters * milk_price
    
    print(f"Total Liters: {total_liters},  Total Value: {total_value}, Milk Price: {milk_price}")

    return {
        "daily_production": daily_production,
        "animal_production": animal_production,
        "statistics": {
            "total_liters": total_liters,
            "total_animals": total_animals,
            "total_value": total_value,
            "milk_price": milk_price
        }
    }

@app.get("/api/milk/animals")
async def api_milk_animals():
    """Obtém a lista de todos os animais."""
    return milk_db.get_animals()

@app.get("/api/milk/production")
async def api_milk_production(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    animal_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    """Obtém registros de produção de leite com paginação e filtros."""
    entries = milk_db.get_milk_production_entries(page, page_size, animal_id, start_date, end_date)
    total_entries = milk_db.count_milk_production_entries(animal_id, start_date, end_date)
    total_pages = (total_entries + page_size - 1) // page_size if total_entries > 0 else 1
    
    return {
        "items": entries,
        "page": page,
        "page_size": page_size,
        "total_items": total_entries,
        "total_pages": total_pages
    }

@app.get("/api/milk/production/{entry_id}")
async def api_milk_production_entry(entry_id: int = Path(..., title="ID do registro de produção")):
    """Obtém um registro de produção de leite por ID."""
    entry = milk_db.get_milk_production_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return entry

@app.post("/api/milk/production")
async def create_milk_production_entry(entry: MilkProductionEntry): # Usando o modelo Pydantic
    """Cria um novo registro de produção de leite."""
    # Verificar se o animal existe
    animal = milk_db.get_animal(entry.animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal não encontrado")

    production_id = milk_db.create_milk_production_entry(
        animal_id=entry.animal_id,
        production_date=entry.production_date,
        liters_produced=entry.quantity,
        period=entry.period,
        notes=entry.notes
        # user_id não é passado aqui, pois não está no modelo MilkProductionEntry
        # Se precisar, adicione-o ao MilkProductionEntry e inclua-o na chamada.
    )
    if not production_id:
        raise HTTPException(status_code=500, detail="Erro ao criar registro")
    return milk_db.get_milk_production_entry(production_id)

@app.put("/api/milk/production/{entry_id}")
async def update_milk_production_entry(entry_id: int, entry_update: MilkProductionUpdate): # Usando o modelo Pydantic
    """Atualiza um registro de produção de leite."""
    # Verificar se o registro existe
    existing_entry = milk_db.get_milk_production_entry(entry_id)
    if not existing_entry:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    success = milk_db.update_milk_production_entry(
        entry_id=entry_id,
        liters_produced=entry_update.quantity,
        period=entry_update.period,
        notes=entry_update.notes
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao atualizar registro")
    
    return milk_db.get_milk_production_entry(entry_id)

@app.delete("/api/milk/production/{entry_id}")
async def delete_milk_production_entry(entry_id: int):
    """Exclui um registro de produção de leite."""
    existing_entry = milk_db.get_milk_production_entry(entry_id)
    if not existing_entry:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    success = milk_db.delete_milk_production_entry(entry_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao excluir registro")
    
    return {"success": True, "message": f"Registro {entry_id} excluído com sucesso"}


# ... (imports and other app setup) ...

# --- Rotas diretas para /api/milk/... ---

# Prioritize specific animal counts FIRST
@app.get("/api/animals/total_count")
async def get_animal_count():
    """Retorna a quantidade total de animais registrados."""
    try:
        count: int = milk_db.count_animals()
        return {"total_animals": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter a contagem de animais: {str(e)}")

@app.get("/api/animals/active_count")
async def api_get_active_animals_count():
    """
    **Retorna a quantidade total de animais com status 'Ativo'.**
    
    Considera animais com status 'Ativo' ou `null` (None) como ativos.
    """
    try:
        active_count = milk_db.get_active_animals_count()
        return {"active_animals_count": active_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor ao contar animais ativos: {str(e)}")

# Now, define the more general route that uses a path parameter
@app.get("/api/milk/animals/{animal_id}")
async def get_animal(animal_id: int = Path(..., title="ID do animal")):
    """Obtém um animal pelo ID."""
    try:
        animal = milk_db.get_animal(animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        return animal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter animal: {str(e)}")

# ... (other /api/milk routes like /production, /dashboard etc.) ...

# Inicialização da aplicação
if __name__ == "__main__":
    import uvicorn
    port = API_PORT
    # Para execução local, use a string de importação
    if DOCKER_ENV == "true":
        # No Docker, use o objeto app diretamente
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # Fora do Docker, use a string de importação para habilitar o reload
        uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)