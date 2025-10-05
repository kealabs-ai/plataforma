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
from milk_price import router as milk_price_router
from beef_cattle import router as beef_cattle_router
from beef_cattle_test import router as beef_cattle_test_router
from beef_cattle_simple import router as beef_cattle_simple_router
from beef_cattle_direct import router as beef_cattle_direct_router
from beef_cattle_mock import router as beef_cattle_mock_router
# Importar os novos routers simplificados
from floriculture import router as floriculture_router
from landscaping import router as landscaping_router
from whatsapp_integration import router as whatsapp_router

# Importa a instância do banco de dados (certifique-se de que milk_db está acessível)
from database_queries.milk_database_query import * # Importa a instância global

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Kealabs Intelligence API",
    description="API para a plataforma Kealabs Intelligence",
    version="1.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8501", "http://localhost:8000", "http://localhost:3000"],  # Permite todas as origens para desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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
app.include_router(milk_price_router)
app.include_router(beef_cattle_router)
app.include_router(beef_cattle_test_router)
app.include_router(beef_cattle_simple_router)
app.include_router(beef_cattle_direct_router)
app.include_router(beef_cattle_mock_router)
# Incluir os novos routers sem prefixo adicional, pois já têm seus próprios prefixos
app.include_router(floriculture_router)
app.include_router(landscaping_router)
app.include_router(whatsapp_router)

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

# Rota de status para verificação de saúde do servidor
@app.get("/status")
async def get_status():
    return {"status": "online", "version": "1.0.0", "message": "API is running correctly"}

# Rota para resetar conexão do banco
@app.post("/reset-db")
async def reset_database_connection():
    from data.connection import reset_connection_pool
    try:
        reset_connection_pool()
        return {"status": "success", "message": "Pool de conexões resetado"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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

# Direct beef cattle endpoints - usando dados reais do banco de dados
@app.get("/api/beef_cattle_mock/dashboard/summary")
async def beef_cattle_dashboard_summary():
    from backend.beef_cattle_database import beef_cattle_db
    try:
        # Buscar dados reais do banco de dados
        return beef_cattle_db.get_dashboard_summary()
    except Exception as e:
        # Em caso de erro, retornar dados mockados
        return {
            "total_cattle": 5,
            "cattle_by_status": [
                {"status": "Em Engorda", "count": 4},
                {"status": "Vendido", "count": 1}
            ],
            "average_weight": 460.0,
            "monthly_sales": 11700.00
        }

@app.get("/api/beef_cattle_mock/")
async def beef_cattle_list():
    from backend.beef_cattle_database import beef_cattle_db
    try:
        # Buscar dados reais do banco de dados
        return beef_cattle_db.get_all_beef_cattle({})
    except Exception as e:
        # Em caso de erro, retornar dados mockados
        return [
            {
                "id": 1,
                "official_id": "BG001",
                "name": "Sultão",
                "birth_date": "2023-01-15",
                "breed": "Nelore",
                "gender": "M",
                "entry_date": "2024-01-10",
                "entry_weight": 380.5,
                "current_weight": 450.2,
                "target_weight": 550.0,
                "status": "Em Engorda",
                "expected_finish_date": "2024-12-15",
                "notes": "Animal saudável, boa conversão alimentar",
                "created_at": "2024-01-10T00:00:00",
                "updated_at": "2024-04-10T00:00:00"
            },
            {
                "id": 2,
                "official_id": "BG002",
                "name": "Trovão",
                "birth_date": "2023-02-20",
                "breed": "Angus",
                "gender": "M",
                "entry_date": "2024-01-15",
                "entry_weight": 410.0,
                "current_weight": 470.5,
                "target_weight": 580.0,
                "status": "Em Engorda",
                "expected_finish_date": "2024-11-20",
                "notes": "Cruzamento industrial, alto ganho diário",
                "created_at": "2024-01-15T00:00:00",
                "updated_at": "2024-04-15T00:00:00"
            }
        ]

@app.get("/api/beef_cattle_mock/sales")
async def beef_cattle_sales():
    from backend.beef_cattle_database import beef_cattle_db
    try:
        # Buscar dados reais do banco de dados
        return beef_cattle_db.get_sale_records({})
    except Exception as e:
        # Em caso de erro, retornar dados mockados
        return [
            {
                "id": 1,
                "cattle_id": 5,
                "official_id": "BG005",
                "name": "Relâmpago",
                "sale_date": "2024-03-20",
                "final_weight": 520.0,
                "price_per_kg": 22.50,
                "total_value": 11700.00,
                "buyer": "Frigorífico São José",
                "notes": "Venda antecipada por bom desempenho",
                "user_id": 1,
                "created_at": "2024-03-20T00:00:00"
            }
        ]

@app.get("/api/beef_cattle_mock/dashboard/weight-gain")
async def beef_cattle_weight_gain():
    from backend.beef_cattle_database import beef_cattle_db
    try:
        # Buscar dados reais do banco de dados
        return beef_cattle_db.get_weight_gain_data({})
    except Exception as e:
        # Em caso de erro, retornar dados mockados
        return [
            {
                "id": 1,
                "official_id": "BG001",
                "name": "Sultão",
                "first_date": "2024-01-10",
                "last_date": "2024-04-10",
                "initial_weight": 380.5,
                "current_weight": 450.2,
                "days": 90,
                "weight_gain": 69.7,
                "daily_gain": 0.77
            },
            {
                "id": 2,
                "official_id": "BG002",
                "name": "Trovão",
                "first_date": "2024-01-15",
                "last_date": "2024-04-15",
                "initial_weight": 410.0,
                "current_weight": 470.5,
                "days": 90,
                "weight_gain": 60.5,
                "daily_gain": 0.67
            }
        ]

@app.get("/api/beef_cattle/dashboard/weight-gain")
async def beef_cattle_weight_gain_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    from backend.beef_cattle_database import beef_cattle_db
    try:
        # Buscar dados reais do banco de dados
        data = beef_cattle_db.get_weight_gain_data({})
        
        # Gerar mais dados para teste de paginação
        if len(data) < 30:
            base_data = data.copy() if data else []
            for i in range(1, 40):
                if len(base_data) > 0:
                    for item in base_data:
                        new_item = item.copy()
                        new_item["id"] = item["id"] + i * 100
                        new_item["official_id"] = f"BG{1000 + i}"
                        new_item["name"] = f"Animal {i}"
                        data.append(new_item)
                        if len(data) >= 40:
                            break
                    if len(data) >= 40:
                        break
        
        # Aplicar paginação manualmente
        total_items = len(data)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Calcular índices de início e fim para a página atual
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_items)
        
        # Obter itens da página atual
        items = data[start_idx:end_idx] if start_idx < total_items else []
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        # Em caso de erro, retornar dados mockados
        mock_data = [
            {
                "id": 1,
                "official_id": "BG001",
                "name": "Sultão",
                "first_date": "2024-01-10",
                "last_date": "2024-04-10",
                "initial_weight": 380.5,
                "current_weight": 450.2,
                "days": 90,
                "weight_gain": 69.7,
                "daily_gain": 0.77
            },
            {
                "id": 2,
                "official_id": "BG002",
                "name": "Trovão",
                "first_date": "2024-01-15",
                "last_date": "2024-04-15",
                "initial_weight": 410.0,
                "current_weight": 470.5,
                "days": 90,
                "weight_gain": 60.5,
                "daily_gain": 0.67
            }
        ]
        
        # Gerar mais dados para teste de paginação
        for i in range(1, 40):
            new_item = mock_data[0].copy()
            new_item["id"] = 100 + i
            new_item["official_id"] = f"BG{1000 + i}"
            new_item["name"] = f"Animal {i}"
            mock_data.append(new_item)
        
        # Aplicar paginação aos dados mockados
        total_items = len(mock_data)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Calcular índices de início e fim para a página atual
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_items)
        
        # Obter itens da página atual
        items = mock_data[start_idx:end_idx] if start_idx < total_items else []
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }

@app.get("/api/beef_cattle_direct_test")
async def beef_cattle_direct_test():
    return {"message": "Direct beef cattle test endpoint is working"}

# Rota para suprimir logs do Chrome DevTools
@app.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools():
    return {}

# Webhook do WhatsApp
@app.post("/webhook/whatsapp")
async def whatsapp_webhook_main(data: dict):
    """Webhook principal para receber eventos do WhatsApp"""
    print(f"Webhook WhatsApp recebido: {data}")
    return {"status": "received"}

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