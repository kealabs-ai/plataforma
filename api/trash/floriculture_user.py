from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from pydantic import BaseModel, validator, Field
import sys
import os

# Adiciona o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Importação simulada de autenticação
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/floriculture/user",
    tags=["Floriculture User"],
    responses={404: {"description": "Not found"}},
)

# Modelos Pydantic
class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str

class UserPreference(BaseModel):
    user_id: int
    preferred_flowers: List[str] = []
    preferred_notification_method: str = "email"
    notification_frequency: str = "daily"
    dashboard_layout: Dict[str, Any] = {}

class UserPreferenceResponse(UserPreference):
    id: int
    created_at: datetime
    updated_at: datetime

class UserActivity(BaseModel):
    user_id: int
    activity_type: str  # "cultivation", "harvest", "treatment", "sale"
    activity_id: int
    timestamp: datetime
    details: Dict[str, Any] = {}

class UserActivityResponse(UserActivity):
    id: int

class UserNotification(BaseModel):
    user_id: int
    title: str
    message: str
    notification_type: str  # "alert", "reminder", "info"
    related_entity_type: Optional[str] = None  # "flower", "greenhouse", "harvest"
    related_entity_id: Optional[int] = None
    is_read: bool = False
    created_at: datetime

class UserNotificationResponse(UserNotification):
    id: int

class PaginatedResponse(BaseModel):
    items: List[Any]
    page: int
    page_size: int
    total_items: int
    total_pages: int

# Endpoints para Preferências do Usuário
@router.get("/preferences", response_model=UserPreferenceResponse)
async def get_user_preferences(current_user: User = Depends(get_current_user)):
    """
    Obtém as preferências do usuário atual.
    """
    try:
        # Simulação de dados
        return {
            "id": 1,
            "user_id": current_user.id,
            "preferred_flowers": ["Rosa", "Orquídea", "Tulipa"],
            "preferred_notification_method": "email",
            "notification_frequency": "daily",
            "dashboard_layout": {
                "charts_order": ["species", "harvest", "sales", "quality"],
                "show_upcoming_harvests": True,
                "show_recent_sales": True
            },
            "created_at": datetime(2024, 1, 1, 0, 0),
            "updated_at": datetime(2024, 4, 1, 10, 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter preferências: {str(e)}")

@router.put("/preferences", response_model=UserPreferenceResponse)
async def update_user_preferences(
    preferences: UserPreference = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza as preferências do usuário atual.
    """
    try:
        # Verificar se o usuário está atualizando suas próprias preferências
        if preferences.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Não é permitido atualizar preferências de outro usuário")
        
        # Simulação de atualização
        return {
            "id": 1,
            "user_id": current_user.id,
            "preferred_flowers": preferences.preferred_flowers,
            "preferred_notification_method": preferences.preferred_notification_method,
            "notification_frequency": preferences.notification_frequency,
            "dashboard_layout": preferences.dashboard_layout,
            "created_at": datetime(2024, 1, 1, 0, 0),
            "updated_at": datetime.now()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar preferências: {str(e)}")

# Endpoints para Atividades do Usuário
@router.get("/activities", response_model=PaginatedResponse)
async def get_user_activities(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    activity_type: Optional[str] = Query(None, description="Filtrar por tipo de atividade"),
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém o histórico de atividades do usuário atual.
    """
    try:
        # Dados simulados para demonstração
        items = [
            {
                "id": 1,
                "user_id": current_user.id,
                "activity_type": "cultivation",
                "activity_id": 1,
                "timestamp": datetime(2024, 3, 15, 10, 0),
                "details": {
                    "action": "create",
                    "species": "Rosa",
                    "variety": "Híbrida de Chá",
                    "quantity": 500
                }
            },
            {
                "id": 2,
                "user_id": current_user.id,
                "activity_type": "harvest",
                "activity_id": 1,
                "timestamp": datetime(2024, 6, 15, 9, 30),
                "details": {
                    "action": "create",
                    "flower_id": 1,
                    "quantity": 200,
                    "quality_grade": "A"
                }
            },
            {
                "id": 3,
                "user_id": current_user.id,
                "activity_type": "treatment",
                "activity_id": 1,
                "timestamp": datetime(2024, 4, 10, 14, 15),
                "details": {
                    "action": "create",
                    "flower_id": 1,
                    "treatment_type": "Fertilização",
                    "product_used": "NPK 10-10-10"
                }
            }
        ]
        
        # Aplicar filtros
        if activity_type:
            items = [item for item in items if activity_type.lower() == item["activity_type"].lower()]
        
        if start_date:
            items = [item for item in items if item["timestamp"].date() >= start_date]
        
        if end_date:
            items = [item for item in items if item["timestamp"].date() <= end_date]
        
        # Paginação
        total_items = len(items)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_items = items[start_idx:end_idx]
        
        return {
            "items": paginated_items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter atividades: {str(e)}")

# Endpoints para Notificações do Usuário
@router.get("/notifications", response_model=PaginatedResponse)
async def get_user_notifications(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    is_read: Optional[bool] = Query(None, description="Filtrar por status de leitura"),
    notification_type: Optional[str] = Query(None, description="Filtrar por tipo de notificação"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém as notificações do usuário atual.
    """
    try:
        # Dados simulados para demonstração
        items = [
            {
                "id": 1,
                "user_id": current_user.id,
                "title": "Colheita Próxima",
                "message": "A colheita de Rosas está programada para os próximos 7 dias.",
                "notification_type": "reminder",
                "related_entity_type": "flower",
                "related_entity_id": 1,
                "is_read": False,
                "created_at": datetime(2024, 6, 8, 8, 0)
            },
            {
                "id": 2,
                "user_id": current_user.id,
                "title": "Alerta de Temperatura",
                "message": "A temperatura na Estufa Principal está acima do ideal (28°C).",
                "notification_type": "alert",
                "related_entity_type": "greenhouse",
                "related_entity_id": 1,
                "is_read": True,
                "created_at": datetime(2024, 6, 7, 14, 30)
            },
            {
                "id": 3,
                "user_id": current_user.id,
                "title": "Venda Registrada",
                "message": "Uma venda de 150 rosas foi registrada com sucesso.",
                "notification_type": "info",
                "related_entity_type": "sale",
                "related_entity_id": 1,
                "is_read": False,
                "created_at": datetime(2024, 6, 6, 16, 45)
            }
        ]
        
        # Aplicar filtros
        if is_read is not None:
            items = [item for item in items if item["is_read"] == is_read]
        
        if notification_type:
            items = [item for item in items if notification_type.lower() == item["notification_type"].lower()]
        
        # Paginação
        total_items = len(items)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_items = items[start_idx:end_idx]
        
        return {
            "items": paginated_items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter notificações: {str(e)}")

@router.put("/notifications/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int = Path(..., description="ID da notificação"),
    current_user: User = Depends(get_current_user)
):
    """
    Marca uma notificação como lida.
    """
    try:
        # Simulação de atualização
        return {"message": f"Notificação {notification_id} marcada como lida"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao marcar notificação como lida: {str(e)}")

@router.put("/notifications/read-all")
async def mark_all_notifications_as_read(current_user: User = Depends(get_current_user)):
    """
    Marca todas as notificações do usuário como lidas.
    """
    try:
        # Simulação de atualização
        return {"message": "Todas as notificações foram marcadas como lidas"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao marcar notificações como lidas: {str(e)}")

# Dashboard personalizado do usuário
@router.get("/dashboard")
async def get_user_dashboard(current_user: User = Depends(get_current_user)):
    """
    Obtém dados para o dashboard personalizado do usuário.
    """
    try:
        # Simulação de dados personalizados com base nas preferências do usuário
        return {
            "user_info": {
                "id": current_user.id,
                "username": current_user.username,
                "full_name": current_user.full_name
            },
            "recent_activities": [
                {
                    "id": 1,
                    "activity_type": "cultivation",
                    "timestamp": datetime(2024, 3, 15, 10, 0),
                    "summary": "Criou cultivo de 500 Rosas"
                },
                {
                    "id": 2,
                    "activity_type": "harvest",
                    "timestamp": datetime(2024, 6, 15, 9, 30),
                    "summary": "Registrou colheita de 200 Rosas"
                }
            ],
            "upcoming_harvests": [
                {
                    "id": 1,
                    "species": "Rosa",
                    "variety": "Híbrida de Chá",
                    "expected_harvest_date": date(2024, 6, 15),
                    "estimated_quantity": 300,
                    "days_remaining": 7
                },
                {
                    "id": 2,
                    "species": "Tulipa",
                    "variety": "Darwin Híbrida",
                    "expected_harvest_date": date(2024, 5, 10),
                    "estimated_quantity": 1000,
                    "days_remaining": 14
                }
            ],
            "preferred_flowers_stats": [
                {
                    "species": "Rosa",
                    "total_cultivated": 500,
                    "total_harvested": 200,
                    "total_sales": 150,
                    "revenue": 750.0
                },
                {
                    "species": "Orquídea",
                    "total_cultivated": 300,
                    "total_harvested": 0,
                    "total_sales": 0,
                    "revenue": 0.0
                },
                {
                    "species": "Tulipa",
                    "total_cultivated": 1000,
                    "total_harvested": 0,
                    "total_sales": 0,
                    "revenue": 0.0
                }
            ],
            "unread_notifications_count": 2
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dashboard personalizado: {str(e)}")

# Endpoint para relatórios personalizados
@router.post("/reports")
async def generate_custom_report(
    start_date: date = Body(...),
    end_date: date = Body(...),
    report_type: str = Body(...),  # "production", "sales", "treatments", "all"
    flower_species: Optional[List[str]] = Body(None),
    include_charts: bool = Body(True),
    current_user: User = Depends(get_current_user)
):
    """
    Gera um relatório personalizado para o usuário.
    """
    try:
        # Simulação de geração de relatório
        return {
            "report_id": 1,
            "user_id": current_user.id,
            "report_type": report_type,
            "start_date": start_date,
            "end_date": end_date,
            "generated_at": datetime.now(),
            "download_url": f"/api/floriculture/user/reports/1/download",
            "summary": {
                "total_flowers_cultivated": 1800,
                "total_flowers_harvested": 350,
                "total_sales": 150,
                "total_revenue": 750.0,
                "total_treatments": 15
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")

@router.get("/reports/{report_id}/download")
async def download_report(
    report_id: int = Path(..., description="ID do relatório"),
    current_user: User = Depends(get_current_user)
):
    """
    Faz o download de um relatório gerado.
    """
    try:
        # Simulação de download
        return {
            "content": "Conteúdo do relatório em formato base64",
            "filename": f"floriculture_report_{report_id}.pdf",
            "content_type": "application/pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer download do relatório: {str(e)}")