from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from pydantic import BaseModel, validator, Field
from database_queries.landscaping_database_query import *
import json

router = APIRouter(
    prefix="/api/landscaping",
    tags=["Landscaping"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class ProjectBase(BaseModel):
    user_id: int
    name: str
    client_name: str
    area_m2: float
    location: str
    start_date: str
    end_date: Optional[str] = None
    budget: Optional[float] = None
    status: str = "planejamento"
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    user_id: int
    name: Optional[str] = None
    client_name: Optional[str] = None
    area_m2: Optional[float] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[float] = None
    status: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int

class SupplierBase(BaseModel):
    user_id: int
    name: str
    contact_person: str
    phone: str
    email: str
    products: str
    last_contract: Optional[str] = None
    status: str = "Ativo"
    notes: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    products: Optional[str] = None
    last_contract: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class SupplierResponse(SupplierBase):
    id: int

class ServiceBase(BaseModel):
    user_id: int
    service_name: str
    category: str
    description: str
    average_duration: float
    base_price: float
    status: str = "Ativo"

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    average_duration: Optional[float] = None
    base_price: Optional[float] = None
    status: Optional[str] = None

class ServiceResponse(ServiceBase):
    id: int

class QuoteItem(BaseModel):
    service_id: int
    quantity: int
    unit_price: float
    description: Optional[str] = None

class QuoteCreate(BaseModel):
    user_id: int
    client_id: int
    description: str
    created_at: str
    valid_until: str
    total_value: float
    notes: Optional[str] = None
    status: str = "Pendente"
    items: List[QuoteItem]

class QuoteResponse(BaseModel):
    id: int
    user_id: int
    client_id: int
    description: str
    created_at: str
    valid_until: str
    total_value: float
    notes: Optional[str] = None
    status: str = "Pendente"
    items: List[QuoteItem]

class MaintenanceBase(BaseModel):
    user_id: int
    project_id: int
    date: str
    type: str
    description: str
    cost: Optional[float] = None
    duration_hours: Optional[float] = None
    status: str = "concluído"
    notes: Optional[str] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    date: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    duration_hours: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class MaintenanceResponse(MaintenanceBase):
    id: int
    project_name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    page: int
    page_size: int
    total_items: int
    total_pages: int

class MaintenancePaginatedResponse(BaseModel):
    items: List[MaintenanceResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int

class ProjectSummary(BaseModel):
    total_projects: int
    active_projects: int
    completed_projects: int
    cancelled_projects: int

class BudgetSummary(BaseModel):
    total_budget: float
    total_spent: float
    percentage: float

class DashboardResponse(BaseModel):
    projects_summary: ProjectSummary
    budget_summary: BudgetSummary
    projects_by_type: List[Dict[str, Any]]
    tasks_by_status: List[Dict[str, Any]]
    materials_by_category: List[Dict[str, Any]]
    monthly_progress: List[Dict[str, Any]]
    quantity_clients: int

# --- CLIENT MODELS ---
class ClientBase(BaseModel):
    user_id: int
    client_name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    client_type: Optional[str] = None
    industry: Optional[str] = None
    status: str = "Lead"
    last_interaction_date: Optional[str] = None
    next_follow_up_date: Optional[str] = None
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    client_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    client_type: Optional[str] = None
    industry: Optional[str] = None
    status: Optional[str] = None
    last_interaction_date: Optional[str] = None
    next_follow_up_date: Optional[str] = None
    notes: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ClientPaginatedResponse(BaseModel):
    items: List[ClientResponse]
    page: int
    page_size: int
    total_items: int
    total_pages: int

# --- PROJECT ENDPOINTS ---

@router.post("/project", response_model=ProjectResponse)
async def create_project_endpoint(project: ProjectCreate = Body(...)):
    """
    Cria um novo projeto de paisagismo.
    """
    try:
        result = create_project(
            user_id=project.user_id,
            name=project.name,
            client_name=project.client_name,
            area_m2=project.area_m2,
            location=project.location,
            start_date=project.start_date,
            end_date=project.end_date,
            budget=project.budget,
            status=project.status,
            description=project.description
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar projeto de paisagismo")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar projeto de paisagismo: {str(e)}")

@router.get("/project", response_model=PaginatedResponse)
async def get_all_projects_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    status: Optional[str] = Query(None, description="Status do projeto"),
    client_name: Optional[str] = Query(None, description="Nome do cliente")
):
    """
    Obtém todos os projetos de paisagismo com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "status": status,
            "client_name": client_name
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_projects(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_projects(filters, page, page_size)
        
        # Processar os itens para garantir que os campos estejam no formato correto
        for item in items:
            # Garantir que o campo location esteja presente
            if "location" not in item and "address" in item:
                item["location"] = item["address"]
            elif "location" not in item:
                item["location"] = ""  # Valor padrão se não existir
                
            # Converter campos de data para string
            if "start_date" in item and isinstance(item["start_date"], date):
                item["start_date"] = item["start_date"].isoformat()
                
            if "end_date" in item and isinstance(item["end_date"], date):
                item["end_date"] = item["end_date"].isoformat()
                
            if "created_at" in item and isinstance(item["created_at"], datetime):
                item["created_at"] = item["created_at"].isoformat()
                
            if "updated_at" in item and isinstance(item["updated_at"], datetime):
                item["updated_at"] = item["updated_at"].isoformat()
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter projetos de paisagismo: {str(e)}")

@router.get("/project/{project_id}", response_model=ProjectResponse)
async def get_project_endpoint(project_id: int = Path(..., description="ID do projeto")):
    """
    Obtém um projeto específico de paisagismo pelo ID.
    """
    try:
        result = get_project(project_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado")
        
        # Garantir que o campo location esteja presente
        if "location" not in result and "address" in result:
            result["location"] = result["address"]
        elif "location" not in result:
            result["location"] = ""  # Valor padrão se não existir
            
        # Converter campos de data para string
        if "start_date" in result and isinstance(result["start_date"], date):
            result["start_date"] = result["start_date"].isoformat()
            
        if "end_date" in result and isinstance(result["end_date"], date):
            result["end_date"] = result["end_date"].isoformat()
            
        if "created_at" in result and isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
            
        if "updated_at" in result and isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter projeto: {str(e)}")

@router.post("/project/{project_id}", response_model=ProjectResponse)
async def update_project_endpoint(
    project_id: int = Path(..., description="ID do projeto"),
    project_data: ProjectUpdate = Body(...)
):
    """
    Atualiza um projeto de paisagismo.
    """
    try:
        # Extrair user_id e outros dados do corpo da requisição
        data_dict = project_data.dict()
        user_id = data_dict.pop("user_id", None)
        
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id é obrigatório no corpo da requisição")
            
        update_data = {k: v for k, v in data_dict.items() if v is not None}
        result = update_project(project_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado ou não pertence ao usuário")
        
        # Garantir que o campo location esteja presente
        if "location" not in result and "address" in result:
            result["location"] = result["address"]
        elif "location" not in result:
            result["location"] = ""  # Valor padrão se não existir
            
        # Converter campos de data para string
        if "start_date" in result and isinstance(result["start_date"], date):
            result["start_date"] = result["start_date"].isoformat()
            
        if "end_date" in result and isinstance(result["end_date"], date):
            result["end_date"] = result["end_date"].isoformat()
            
        if "created_at" in result and isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
            
        if "updated_at" in result and isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar projeto: {str(e)}")

@router.delete("/project/{project_id}")
async def delete_project_endpoint(
    project_id: int = Path(..., description="ID do projeto"),
    user_id: int = Query(..., description="ID do usuário")
):
    """
    Remove um projeto de paisagismo.
    """
    try:
        success = delete_project(project_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado ou não pertence ao usuário")
        return {"message": f"Projeto com ID {project_id} removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover projeto: {str(e)}")

@router.patch("/project/{project_id}/status")
async def update_project_status(
    project_id: int = Path(..., description="ID do projeto"),
    user_id: int = Query(..., description="ID do usuário"),
    status: str = Query(..., description="Novo status")
):
    """
    Atualiza apenas o status de um projeto de paisagismo.
    Endpoint otimizado para atualizações rápidas de status no quadro Kanban.
    """
    try:
        # Usar a função update_project para atualizar apenas o status
        update_data = {"status": status}
        result = update_project(project_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado ou não pertence ao usuário")
        
        # Converter campos de data para string
        if "start_date" in result and isinstance(result["start_date"], date):
            result["start_date"] = result["start_date"].isoformat()
            
        if "end_date" in result and isinstance(result["end_date"], date):
            result["end_date"] = result["end_date"].isoformat()
            
        if "created_at" in result and isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
            
        if "updated_at" in result and isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar status do projeto: {str(e)}")

# --- DASHBOARD ENDPOINT ---

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard_data(
    user_id: Optional[int] = Query(None, description="ID do usuário")
):
    """
    Obtém dados resumidos para o dashboard de paisagismo.
    """
    try:
        print("valor do usuário: ", user_id)
        result = get_dashboard_summary(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Não foi possível obter dados do dashboard")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados do dashboard: {str(e)}")

# --- SUPPLIER ENDPOINTS ---

@router.post("/supplier", response_model=SupplierResponse)
async def create_supplier_endpoint(supplier: SupplierCreate = Body(...)):
    """
    Cria um novo fornecedor de paisagismo.
    """
    try:
        result = create_supplier(
            user_id=supplier.user_id,
            name=supplier.name,
            contact_person=supplier.contact_person,
            phone=supplier.phone,
            email=supplier.email,
            products=supplier.products,
            last_contract=supplier.last_contract,
            status=supplier.status,
            notes=supplier.notes
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar fornecedor de paisagismo")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar fornecedor de paisagismo: {str(e)}")

@router.get("/supplier", response_model=PaginatedResponse)
async def get_all_suppliers_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    status: Optional[str] = Query(None, description="Status do fornecedor"),
    name: Optional[str] = Query(None, description="Nome do fornecedor")
):
    """
    Obtém todos os fornecedores de paisagismo com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "status": status,
            "name": name
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_suppliers(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_suppliers(filters, page, page_size)
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter fornecedores de paisagismo: {str(e)}")

@router.get("/supplier/{supplier_id}", response_model=SupplierResponse)
async def get_supplier_endpoint(supplier_id: int = Path(..., description="ID do fornecedor")):
    """
    Obtém um fornecedor específico pelo ID.
    """
    try:
        result = get_supplier(supplier_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Fornecedor com ID {supplier_id} não encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter fornecedor: {str(e)}")

@router.post("/supplier/{supplier_id}", response_model=SupplierResponse)
async def update_supplier_endpoint(
    supplier_id: int = Path(..., description="ID do fornecedor"),
    user_id: int = Query(..., description="ID do usuário"),
    supplier_data: SupplierUpdate = Body(...)
):
    """
    Atualiza um fornecedor de paisagismo.
    """
    try:
        update_data = {k: v for k, v in supplier_data.dict().items() if v is not None}
        result = update_supplier(supplier_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Fornecedor com ID {supplier_id} não encontrado ou não pertence ao usuário")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar fornecedor: {str(e)}")

@router.delete("/supplier/{supplier_id}")
async def delete_supplier_endpoint(
    supplier_id: int = Path(..., description="ID do fornecedor"),
    user_id: int = Query(..., description="ID do usuário")
):
    """
    Remove um fornecedor de paisagismo.
    """
    try:
        success = delete_supplier(supplier_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Fornecedor com ID {supplier_id} não encontrado ou não pertence ao usuário")
        return {"message": f"Fornecedor com ID {supplier_id} removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover fornecedor: {str(e)}")

# --- SERVICE ENDPOINTS ---

@router.post("/service", response_model=ServiceResponse)
async def create_service_endpoint(service: ServiceCreate = Body(...)):
    """
    Cria um novo serviço de paisagismo.
    """
    try:
        result = create_service(
            user_id=service.user_id,
            service_name=service.service_name,
            category=service.category,
            description=service.description,
            average_duration=service.average_duration,
            base_price=service.base_price,
            status=service.status
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar serviço de paisagismo")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar serviço de paisagismo: {str(e)}")

@router.get("/service", response_model=PaginatedResponse)
async def get_all_services_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    status: Optional[str] = Query(None, description="Status do serviço"),
    category: Optional[str] = Query(None, description="Categoria do serviço")
):
    """
    Obtém todos os serviços de paisagismo com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "status": status,
            "category": category
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_services(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_services(filters, page, page_size)
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter serviços de paisagismo: {str(e)}")

@router.get("/service/{service_id}", response_model=ServiceResponse)
async def get_service_endpoint(service_id: int = Path(..., description="ID do serviço")):
    """
    Obtém um serviço específico pelo ID.
    """
    try:
        result = get_service(service_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Serviço com ID {service_id} não encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter serviço: {str(e)}")

@router.post("/service/{service_id}", response_model=ServiceResponse)
async def update_service_endpoint(
    service_id: int = Path(..., description="ID do serviço"),
    user_id: int = Query(..., description="ID do usuário"),
    service_data: ServiceUpdate = Body(...)
):
    """
    Atualiza um serviço de paisagismo.
    """
    try:
        update_data = {k: v for k, v in service_data.dict().items() if v is not None}
        result = update_service(service_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Serviço com ID {service_id} não encontrado ou não pertence ao usuário")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar serviço: {str(e)}")

@router.delete("/service/{service_id}")
async def delete_service_endpoint(
    service_id: int = Path(..., description="ID do serviço"),
    user_id: int = Query(..., description="ID do usuário")
):
    """
    Inativa um serviço de paisagismo.
    """
    try:
        # Em vez de excluir, apenas inativa o serviço
        update_data = {"status": "Inativo"}
        result = update_service(service_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Serviço com ID {service_id} não encontrado ou não pertence ao usuário")
        return {"message": f"Serviço com ID {service_id} inativado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inativar serviço: {str(e)}")

# --- QUOTE ENDPOINTS ---

@router.post("/quote", response_model=QuoteResponse)
async def create_quote_endpoint(quote_data: dict = Body(...)):
    """
    Cria um novo orçamento de paisagismo.
    """
    try:
        # Extrair os campos do JSON recebido
        user_id = quote_data.get("user_id")
        client_id = quote_data.get("client_id")
        description = quote_data.get("description")
        created_at = quote_data.get("created_at")
        valid_until = quote_data.get("valid_until")
        total_value = quote_data.get("total_value")
        notes = quote_data.get("notes")
        status = quote_data.get("status", "Pendente")
        items = quote_data.get("items", [])
        
        # Validar campos obrigatórios
        if not all([user_id, client_id, description, valid_until, total_value]):
            raise HTTPException(status_code=400, detail="Campos obrigatórios faltando")
            
        result = create_quote(
            user_id=user_id,
            client_id=client_id,
            description=description,
            created_at=created_at,
            valid_until=valid_until,
            total_value=total_value,
            notes=notes,
            status=status,
            items=items
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar orçamento de paisagismo")
            
        # Ensure datetime fields are strings
        if "created_at" in result and not isinstance(result["created_at"], str):
            if isinstance(result["created_at"], datetime):
                result["created_at"] = result["created_at"].isoformat()
                
        if "valid_until" in result and not isinstance(result["valid_until"], str):
            if isinstance(result["valid_until"], date):
                result["valid_until"] = result["valid_until"].isoformat()
                
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar orçamento de paisagismo: {str(e)}")

@router.get("/quote", response_model=PaginatedResponse)
async def get_all_quotes_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    status: Optional[str] = Query(None, description="Status do orçamento"),
    client: Optional[str] = Query(None, description="Nome do cliente")
):
    """
    Obtém todos os orçamentos de paisagismo com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "status": status,
            "client": client
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_quotes(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_quotes(filters, page, page_size)
        
        # Ensure datetime fields are strings for all items
        for item in items:
            if "created_at" in item and not isinstance(item["created_at"], str):
                if isinstance(item["created_at"], datetime):
                    item["created_at"] = item["created_at"].isoformat()
                    
            if "valid_until" in item and not isinstance(item["valid_until"], str):
                if isinstance(item["valid_until"], date):
                    item["valid_until"] = item["valid_until"].isoformat()
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter orçamentos de paisagismo: {str(e)}")

@router.get("/quote/{quote_id}", response_model=QuoteResponse)
async def get_quote_endpoint(quote_id: int = Path(..., description="ID do orçamento")):
    """
    Obtém um orçamento específico pelo ID.
    """
    try:
        result = get_quote(quote_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Orçamento com ID {quote_id} não encontrado")
            
        # Ensure datetime fields are strings
        if "created_at" in result and not isinstance(result["created_at"], str):
            if isinstance(result["created_at"], datetime):
                result["created_at"] = result["created_at"].isoformat()
                
        if "valid_until" in result and not isinstance(result["valid_until"], str):
            if isinstance(result["valid_until"], date):
                result["valid_until"] = result["valid_until"].isoformat()
                
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter orçamento: {str(e)}")

# --- MAINTENANCE ENDPOINTS ---

@router.post("/maintenance", response_model=MaintenanceResponse)
async def create_maintenance_endpoint(maintenance: MaintenanceCreate = Body(...)):
    """
    Cria um novo registro de manutenção de paisagismo.
    """
    try:
        result = create_maintenance(
            user_id=maintenance.user_id,
            project_id=maintenance.project_id,
            date=maintenance.date,
            type=maintenance.type,
            description=maintenance.description,
            cost=maintenance.cost,
            duration_hours=maintenance.duration_hours,
            status=maintenance.status,
            notes=maintenance.notes
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar registro de manutenção")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar registro de manutenção: {str(e)}")

@router.get("/maintenance", response_model=MaintenancePaginatedResponse)
async def get_all_maintenance_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    project_id: Optional[int] = Query(None, description="ID do projeto"),
    type: Optional[str] = Query(None, description="Tipo de manutenção"),
    status: Optional[str] = Query(None, description="Status da manutenção")
):
    """
    Obtém todos os registros de manutenção com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "project_id": project_id,
            "type": type,
            "status": status
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_maintenance(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_maintenance(filters, page, page_size)
        
        # Garantir que todos os campos estejam presentes
        for item in items:
            # Mapear campos do banco de dados para os campos do modelo
            if "maintenance_date" in item and "date" not in item:
                # Converter datetime.date para string
                if isinstance(item["maintenance_date"], date):
                    item["date"] = item["maintenance_date"].isoformat()
                else:
                    item["date"] = item["maintenance_date"]
            elif "date" in item and isinstance(item["date"], date):
                # Converter datetime.date para string se já existir
                item["date"] = item["date"].isoformat()
                
            if "maintenance_type" in item and "type" not in item:
                item["type"] = item["maintenance_type"]
            if "hours_spent" in item and "duration_hours" not in item:
                item["duration_hours"] = item["hours_spent"]
            
            # Garantir que campos opcionais estejam presentes
            if "created_at" not in item:
                item["created_at"] = None
            elif isinstance(item["created_at"], datetime):
                item["created_at"] = item["created_at"].isoformat()
                
            if "updated_at" not in item:
                item["updated_at"] = None
            elif isinstance(item["updated_at"], datetime):
                item["updated_at"] = item["updated_at"].isoformat()
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de manutenção: {str(e)}")

@router.get("/maintenance/{maintenance_id}", response_model=MaintenanceResponse)
async def get_maintenance_endpoint(maintenance_id: int = Path(..., description="ID da manutenção")):
    """
    Obtém um registro específico de manutenção pelo ID.
    """
    try:
        result = get_maintenance(maintenance_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Registro de manutenção com ID {maintenance_id} não encontrado")
        
        # Mapear campos do banco de dados para os campos do modelo
        if "maintenance_date" in result and "date" not in result:
            # Converter datetime.date para string
            if isinstance(result["maintenance_date"], date):
                result["date"] = result["maintenance_date"].isoformat()
            else:
                result["date"] = result["maintenance_date"]
        elif "date" in result and isinstance(result["date"], date):
            # Converter datetime.date para string se já existir
            result["date"] = result["date"].isoformat()
            
        if "maintenance_type" in result and "type" not in result:
            result["type"] = result["maintenance_type"]
        if "hours_spent" in result and "duration_hours" not in result:
            result["duration_hours"] = result["hours_spent"]
        
        # Garantir que campos opcionais estejam presentes
        if "created_at" not in result:
            result["created_at"] = None
        elif isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
            
        if "updated_at" not in result:
            result["updated_at"] = None
        elif isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registro de manutenção: {str(e)}")

@router.post("/maintenance/{maintenance_id}", response_model=MaintenanceResponse)
async def update_maintenance_endpoint(
    maintenance_id: int = Path(..., description="ID da manutenção"),
    maintenance_data: MaintenanceUpdate = Body(...)
):
    """
    Atualiza um registro de manutenção de paisagismo.
    """
    try:
        # Obter o registro atual para verificar o user_id
        current_maintenance = get_maintenance(maintenance_id)
        if not current_maintenance:
            raise HTTPException(status_code=404, detail=f"Registro de manutenção com ID {maintenance_id} não encontrado")
        
        user_id = current_maintenance["user_id"]
        
        # Filtrar apenas os campos não nulos
        update_data = {k: v for k, v in maintenance_data.dict().items() if v is not None}
        
        # Atualizar o registro
        result = update_maintenance(maintenance_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Registro de manutenção com ID {maintenance_id} não encontrado ou não pertence ao usuário")
        
        # Mapear campos do banco de dados para os campos do modelo
        if "maintenance_date" in result and "date" not in result:
            # Converter datetime.date para string
            if isinstance(result["maintenance_date"], date):
                result["date"] = result["maintenance_date"].isoformat()
            else:
                result["date"] = result["maintenance_date"]
        elif "date" in result and isinstance(result["date"], date):
            # Converter datetime.date para string se já existir
            result["date"] = result["date"].isoformat()
            
        if "maintenance_type" in result and "type" not in result:
            result["type"] = result["maintenance_type"]
        if "hours_spent" in result and "duration_hours" not in result:
            result["duration_hours"] = result["hours_spent"]
        
        # Garantir que campos opcionais estejam presentes
        if "created_at" not in result:
            result["created_at"] = None
        elif isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
            
        if "updated_at" not in result:
            result["updated_at"] = None
        elif isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar registro de manutenção: {str(e)}")

# --- CLIENT ENDPOINTS ---

@router.post("/client", response_model=ClientResponse)
async def create_client_endpoint(client: ClientCreate = Body(...)):
    """
    Cria um novo cliente de paisagismo.
    """
    try:
        result = create_client(
            user_id=client.user_id,
            client_name=client.client_name,
            contact_person=client.contact_person,
            email=client.email,
            phone_number=client.phone_number,
            address=client.address,
            city=client.city,
            state=client.state,
            zip_code=client.zip_code,
            client_type=client.client_type,
            industry=client.industry,
            status=client.status,
            last_interaction_date=client.last_interaction_date,
            next_follow_up_date=client.next_follow_up_date,
            notes=client.notes
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar cliente de paisagismo")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente de paisagismo: {str(e)}")

@router.get("/client", response_model=ClientPaginatedResponse)
async def get_all_clients_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    status: Optional[str] = Query(None, description="Status do cliente"),
    client_name: Optional[str] = Query(None, description="Nome do cliente"),
    industry: Optional[str] = Query(None, description="Setor do cliente")
):
    """
    Obtém todos os clientes de paisagismo com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "status": status,
            "client_name": client_name,
            "industry": industry
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_clients(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_clients(filters, page, page_size)
        
        # Converter campos datetime para string
        for item in items:
            if "created_at" in item and isinstance(item["created_at"], datetime):
                item["created_at"] = item["created_at"].isoformat()
            if "updated_at" in item and isinstance(item["updated_at"], datetime):
                item["updated_at"] = item["updated_at"].isoformat()
            if "last_interaction_date" in item and isinstance(item["last_interaction_date"], date):
                item["last_interaction_date"] = item["last_interaction_date"].isoformat()
            if "next_follow_up_date" in item and isinstance(item["next_follow_up_date"], date):
                item["next_follow_up_date"] = item["next_follow_up_date"].isoformat()
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter clientes de paisagismo: {str(e)}")

@router.get("/client/{client_id}", response_model=ClientResponse)
async def get_client_endpoint(client_id: int = Path(..., description="ID do cliente")):
    """
    Obtém um cliente específico pelo ID.
    """
    try:
        result = get_client(client_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Cliente com ID {client_id} não encontrado")
        
        # Converter campos datetime para string
        if "created_at" in result and isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
        if "updated_at" in result and isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
        if "last_interaction_date" in result and isinstance(result["last_interaction_date"], date):
            result["last_interaction_date"] = result["last_interaction_date"].isoformat()
        if "next_follow_up_date" in result and isinstance(result["next_follow_up_date"], date):
            result["next_follow_up_date"] = result["next_follow_up_date"].isoformat()
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter cliente: {str(e)}")

@router.post("/client/{client_id}", response_model=ClientResponse)
async def update_client_endpoint(
    client_id: int = Path(..., description="ID do cliente"),
    user_id: int = Query(..., description="ID do usuário"),
    client_data: ClientUpdate = Body(...)
):
    """
    Atualiza um cliente de paisagismo.
    """
    try:
        update_data = {k: v for k, v in client_data.dict().items() if v is not None}
        result = update_client(client_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Cliente com ID {client_id} não encontrado ou não pertence ao usuário")
        
        # Converter campos datetime para string
        if "created_at" in result and isinstance(result["created_at"], datetime):
            result["created_at"] = result["created_at"].isoformat()
        if "updated_at" in result and isinstance(result["updated_at"], datetime):
            result["updated_at"] = result["updated_at"].isoformat()
        if "last_interaction_date" in result and isinstance(result["last_interaction_date"], date):
            result["last_interaction_date"] = result["last_interaction_date"].isoformat()
        if "next_follow_up_date" in result and isinstance(result["next_follow_up_date"], date):
            result["next_follow_up_date"] = result["next_follow_up_date"].isoformat()
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")

@router.delete("/client/{client_id}")
async def delete_client_endpoint(
    client_id: int = Path(..., description="ID do cliente"),
    user_id: int = Query(..., description="ID do usuário")
):
    """
    Inativa um cliente de paisagismo.
    """
    try:
        # Em vez de excluir, apenas inativa o cliente
        update_data = {"status": "Inativo"}
        result = update_client(client_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Cliente com ID {client_id} não encontrado ou não pertence ao usuário")
        return {"message": f"Cliente com ID {client_id} inativado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inativar cliente: {str(e)}")