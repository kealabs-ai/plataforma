from fastapi import APIRouter, Depends, HTTPException, Path, Query, Body
from typing import Optional, List

from models.landscaping import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse,
    SupplierCreate, SupplierUpdate, SupplierResponse,
    ServiceCreate, ServiceUpdate, ServiceResponse,
    QuoteCreate, QuoteUpdate, QuoteResponse,
    PaginatedResponse
)
from models.user import User
from auth.dependencies import get_current_user
from database import landscaping_db

router = APIRouter(prefix="/landscaping/endpoints", tags=["Paisagismo"])

# Endpoints para Projetos de Paisagismo
@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo projeto de paisagismo.
    """
    try:
        result = landscaping_db.create_project(
            user_id=current_user.id,
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

@router.get("/projects", response_model=PaginatedResponse)
async def get_all_projects(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    client_name: Optional[str] = Query(None, description="Filtrar por cliente"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os projetos de paisagismo, com opções de filtro e paginação.
    """
    try:
        filters = {
            "status": status,
            "client_name": client_name,
            "user_id": current_user.id
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_all_projects(filters, page, page_size)
        total_items = landscaping_db.count_projects(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter projetos de paisagismo: {str(e)}")

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int = Path(..., description="ID do projeto"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém um projeto específico de paisagismo pelo ID.
    """
    try:
        project = landscaping_db.get_project(project_id)
        
        if not project:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado")
        
        # Verificar se o projeto pertence ao usuário
        if project['user_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado a este projeto")
        
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter projeto: {str(e)}")

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int = Path(..., description="ID do projeto"),
    project_data: ProjectUpdate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza um projeto de paisagismo.
    """
    try:
        update_data = {k: v for k, v in project_data.dict().items() if v is not None}
        
        result = landscaping_db.update_project(project_id, current_user.id, update_data)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado ou acesso negado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar projeto: {str(e)}")

@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int = Path(..., description="ID do projeto"),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um projeto de paisagismo.
    """
    try:
        success = landscaping_db.delete_project(project_id, current_user.id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado ou acesso negado")
        
        return {"message": f"Projeto com ID {project_id} removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover projeto: {str(e)}")

# Endpoints para Fornecedores de Paisagismo
@router.post("/suppliers", response_model=SupplierResponse)
async def create_supplier(
    supplier: SupplierCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo fornecedor de paisagismo.
    """
    try:
        result = landscaping_db.create_supplier(
            user_id=current_user.id,
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
            raise HTTPException(status_code=500, detail="Erro ao criar fornecedor")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar fornecedor: {str(e)}")

@router.get("/suppliers", response_model=PaginatedResponse)
async def get_all_suppliers(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    name: Optional[str] = Query(None, description="Filtrar por nome"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os fornecedores de paisagismo, com opções de filtro e paginação.
    """
    try:
        filters = {
            "status": status,
            "name": name,
            "user_id": current_user.id
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_all_suppliers(filters, page, page_size)
        total_items = landscaping_db.count_suppliers(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter fornecedores: {str(e)}")

@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: int = Path(..., description="ID do fornecedor"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém um fornecedor específico pelo ID.
    """
    try:
        supplier = landscaping_db.get_supplier(supplier_id)
        
        if not supplier:
            raise HTTPException(status_code=404, detail=f"Fornecedor com ID {supplier_id} não encontrado")
        
        # Verificar se o fornecedor pertence ao usuário
        if supplier['user_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado a este fornecedor")
        
        return supplier
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter fornecedor: {str(e)}")

@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: int = Path(..., description="ID do fornecedor"),
    supplier_data: SupplierUpdate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza um fornecedor.
    """
    try:
        update_data = {k: v for k, v in supplier_data.dict().items() if v is not None}
        
        result = landscaping_db.update_supplier(supplier_id, current_user.id, update_data)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Fornecedor com ID {supplier_id} não encontrado ou acesso negado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar fornecedor: {str(e)}")

@router.delete("/suppliers/{supplier_id}")
async def delete_supplier(
    supplier_id: int = Path(..., description="ID do fornecedor"),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um fornecedor.
    """
    try:
        success = landscaping_db.delete_supplier(supplier_id, current_user.id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Fornecedor com ID {supplier_id} não encontrado ou acesso negado")
        
        return {"message": f"Fornecedor com ID {supplier_id} removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover fornecedor: {str(e)}")

# Endpoints para Serviços de Paisagismo
@router.post("/services", response_model=ServiceResponse)
async def create_service(
    service: ServiceCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo serviço de paisagismo.
    """
    try:
        result = landscaping_db.create_service(
            user_id=current_user.id,
            service_name=service.service_name,
            category=service.category,
            description=service.description,
            average_duration=service.average_duration,
            base_price=service.base_price,
            status=service.status
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar serviço")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar serviço: {str(e)}")

@router.get("/services", response_model=PaginatedResponse)
async def get_all_services(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os serviços de paisagismo, com opções de filtro e paginação.
    """
    try:
        filters = {
            "category": category,
            "status": status,
            "user_id": current_user.id
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_all_services(filters, page, page_size)
        total_items = landscaping_db.count_services(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter serviços: {str(e)}")

# Endpoints para Orçamentos de Paisagismo
@router.post("/quotes", response_model=QuoteResponse)
async def create_quote(
    quote: QuoteCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo orçamento de paisagismo.
    """
    try:
        result = landscaping_db.create_quote(
            user_id=current_user.id,
            client=quote.client,
            description=quote.description,
            created_date=quote.created_date,
            valid_until=quote.valid_until,
            total_value=quote.total_value,
            status=quote.status,
            items=quote.items
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar orçamento")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar orçamento: {str(e)}")

@router.get("/quotes", response_model=PaginatedResponse)
async def get_all_quotes(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    client: Optional[str] = Query(None, description="Filtrar por cliente"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os orçamentos de paisagismo, com opções de filtro e paginação.
    """
    try:
        filters = {
            "client": client,
            "status": status,
            "user_id": current_user.id
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_all_quotes(filters, page, page_size)
        total_items = landscaping_db.count_quotes(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter orçamentos: {str(e)}")

# Endpoints para Manutenção de Paisagismo
@router.post("/maintenance", response_model=MaintenanceResponse)
async def create_maintenance(
    maintenance: MaintenanceCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo registro de manutenção de paisagismo.
    """
    try:
        result = landscaping_db.create_maintenance(
            user_id=current_user.id,
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

@router.get("/maintenance", response_model=PaginatedResponse)
async def get_all_maintenance(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    project_id: Optional[int] = Query(None, description="Filtrar por projeto"),
    type: Optional[str] = Query(None, description="Filtrar por tipo"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os registros de manutenção, com opções de filtro e paginação.
    """
    try:
        filters = {
            "project_id": project_id,
            "type": type,
            "status": status,
            "user_id": current_user.id
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_all_maintenance(filters, page, page_size)
        total_items = landscaping_db.count_maintenance(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de manutenção: {str(e)}")