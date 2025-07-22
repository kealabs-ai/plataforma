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

from backend.landscaping_database_query import landscaping_db
from backend.auth import get_current_user

router = APIRouter(
    prefix="/api/landscaping/endpoints",
    tags=["Landscaping Endpoints"],
    responses={404: {"description": "Not found"}},
)

# Modelos Pydantic
class ProjectBase(BaseModel):
    name: str
    client_name: str
    project_type: str  # Residencial, Comercial, Público
    area_m2: float
    start_date: date
    expected_end_date: Optional[date] = None
    budget: float
    status: str = "Em Andamento"
    address: Optional[str] = None
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client_name: Optional[str] = None
    project_type: Optional[str] = None
    area_m2: Optional[float] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    budget: Optional[float] = None
    status: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TaskBase(BaseModel):
    project_id: int
    task_name: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    status: str = "Pendente"  # Pendente, Em Andamento, Concluída
    assigned_to: Optional[str] = None
    priority: str = "Média"  # Alta, Média, Baixa

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    task_name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime

class MaterialBase(BaseModel):
    project_id: int
    name: str
    category: str  # Plantas, Materiais de Construção, Ferramentas, etc.
    quantity: float
    unit: str
    unit_price: float
    supplier: Optional[str] = None
    purchase_date: Optional[date] = None
    notes: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    supplier: Optional[str] = None
    purchase_date: Optional[date] = None
    notes: Optional[str] = None

class MaterialResponse(MaterialBase):
    id: int
    created_at: datetime
    total_price: float

class PlantingRecordBase(BaseModel):
    project_id: int
    planting_date: date
    plant_type: str
    species: str
    quantity: int
    area_m2: float
    notes: Optional[str] = None

class PlantingRecordCreate(PlantingRecordBase):
    pass

class PlantingRecordResponse(PlantingRecordBase):
    id: int
    created_at: datetime

class PaginatedResponse(BaseModel):
    items: List[Any]
    page: int
    page_size: int
    total_items: int
    total_pages: int

class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str

# Endpoints para Projetos
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
            project_type=project.project_type,
            area_m2=project.area_m2,
            start_date=project.start_date,
            budget=project.budget,
            expected_end_date=project.expected_end_date,
            status=project.status,
            address=project.address,
            description=project.description
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar projeto")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar projeto: {str(e)}")

@router.get("/projects", response_model=PaginatedResponse)
async def get_all_projects(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    project_type: Optional[str] = Query(None, description="Filtrar por tipo de projeto"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    client_name: Optional[str] = Query(None, description="Filtrar por cliente"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os projetos de paisagismo, com opções de filtro e paginação.
    """
    try:
        filters = {
            "project_type": project_type,
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
        raise HTTPException(status_code=500, detail=f"Erro ao obter projetos: {str(e)}")

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int = Path(..., description="ID do projeto"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém um projeto específico pelo ID.
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
    Exclui um projeto de paisagismo.
    """
    try:
        success = landscaping_db.delete_project(project_id, current_user.id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado ou acesso negado")
        
        return {"message": f"Projeto com ID {project_id} excluído com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir projeto: {str(e)}")

# Endpoints para Tarefas
@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Cria uma nova tarefa para um projeto.
    """
    try:
        result = landscaping_db.create_task(
            project_id=task.project_id,
            user_id=current_user.id,
            task_name=task.task_name,
            description=task.description,
            start_date=task.start_date,
            end_date=task.end_date,
            status=task.status,
            assigned_to=task.assigned_to,
            priority=task.priority
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar tarefa: {str(e)}")

@router.get("/tasks/project/{project_id}", response_model=PaginatedResponse)
async def get_project_tasks(
    project_id: int = Path(..., description="ID do projeto"),
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    priority: Optional[str] = Query(None, description="Filtrar por prioridade"),
    assigned_to: Optional[str] = Query(None, description="Filtrar por responsável"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todas as tarefas de um projeto específico, com opções de filtro e paginação.
    """
    try:
        # Verificar se o projeto existe e pertence ao usuário
        project = landscaping_db.get_project(project_id)
        if not project or project['user_id'] != current_user.id:
            raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
        
        filters = {
            "status": status,
            "priority": priority,
            "assigned_to": assigned_to
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_project_tasks(project_id, filters, page, page_size)
        total_items = landscaping_db.count_project_tasks(project_id, filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter tarefas: {str(e)}")

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int = Path(..., description="ID da tarefa"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém uma tarefa específica pelo ID.
    """
    try:
        task = landscaping_db.get_task(task_id)
        
        if not task:
            raise HTTPException(status_code=404, detail=f"Tarefa com ID {task_id} não encontrada")
        
        # Verificar se o usuário tem acesso ao projeto da tarefa
        project = landscaping_db.get_project(task['project_id'])
        if not project or project['user_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado a esta tarefa")
        
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter tarefa: {str(e)}")

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int = Path(..., description="ID da tarefa"),
    task_data: TaskUpdate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza uma tarefa.
    """
    try:
        update_data = {k: v for k, v in task_data.dict().items() if v is not None}
        
        result = landscaping_db.update_task(task_id, current_user.id, update_data)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Tarefa com ID {task_id} não encontrada ou acesso negado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar tarefa: {str(e)}")

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int = Path(..., description="ID da tarefa"),
    current_user: User = Depends(get_current_user)
):
    """
    Exclui uma tarefa.
    """
    try:
        success = landscaping_db.delete_task(task_id, current_user.id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Tarefa com ID {task_id} não encontrada ou acesso negado")
        
        return {"message": f"Tarefa com ID {task_id} excluída com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir tarefa: {str(e)}")

# Endpoints para Materiais
@router.post("/materials", response_model=MaterialResponse)
async def create_material(
    material: MaterialCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Registra um novo material para um projeto.
    """
    try:
        result = landscaping_db.create_material(
            project_id=material.project_id,
            user_id=current_user.id,
            name=material.name,
            category=material.category,
            quantity=material.quantity,
            unit=material.unit,
            unit_price=material.unit_price,
            supplier=material.supplier,
            purchase_date=material.purchase_date,
            notes=material.notes
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar material: {str(e)}")

@router.get("/materials/project/{project_id}", response_model=PaginatedResponse)
async def get_project_materials(
    project_id: int = Path(..., description="ID do projeto"),
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    supplier: Optional[str] = Query(None, description="Filtrar por fornecedor"),
    start_date: Optional[date] = Query(None, description="Data inicial de compra"),
    end_date: Optional[date] = Query(None, description="Data final de compra"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os materiais de um projeto específico, com opções de filtro e paginação.
    """
    try:
        # Verificar se o projeto existe e pertence ao usuário
        project = landscaping_db.get_project(project_id)
        if not project or project['user_id'] != current_user.id:
            raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
        
        filters = {
            "category": category,
            "supplier": supplier,
            "start_date": start_date,
            "end_date": end_date
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_project_materials(project_id, filters, page, page_size)
        total_items = landscaping_db.count_project_materials(project_id, filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter materiais: {str(e)}")

@router.get("/materials/{material_id}", response_model=MaterialResponse)
async def get_material(
    material_id: int = Path(..., description="ID do material"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém um material específico pelo ID.
    """
    try:
        material = landscaping_db.get_material(material_id)
        
        if not material:
            raise HTTPException(status_code=404, detail=f"Material com ID {material_id} não encontrado")
        
        # Verificar se o usuário tem acesso ao projeto do material
        project = landscaping_db.get_project(material['project_id'])
        if not project or project['user_id'] != current_user.id:
            raise HTTPException(status_code=403, detail="Acesso negado a este material")
        
        return material
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter material: {str(e)}")

@router.put("/materials/{material_id}", response_model=MaterialResponse)
async def update_material(
    material_id: int = Path(..., description="ID do material"),
    material_data: MaterialUpdate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza um material.
    """
    try:
        update_data = {k: v for k, v in material_data.dict().items() if v is not None}
        
        result = landscaping_db.update_material(material_id, current_user.id, update_data)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Material com ID {material_id} não encontrado ou acesso negado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar material: {str(e)}")

@router.delete("/materials/{material_id}")
async def delete_material(
    material_id: int = Path(..., description="ID do material"),
    current_user: User = Depends(get_current_user)
):
    """
    Exclui um material.
    """
    try:
        success = landscaping_db.delete_material(material_id, current_user.id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Material com ID {material_id} não encontrado ou acesso negado")
        
        return {"message": f"Material com ID {material_id} excluído com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir material: {str(e)}")

# Endpoints para Registros de Plantio
@router.post("/planting", response_model=PlantingRecordResponse)
async def create_planting_record(
    record: PlantingRecordCreate = Body(...),
    current_user: User = Depends(get_current_user)
):
    """
    Cria um novo registro de plantio para um projeto.
    """
    try:
        result = landscaping_db.create_planting_record(
            project_id=record.project_id,
            user_id=current_user.id,
            planting_date=record.planting_date,
            plant_type=record.plant_type,
            species=record.species,
            quantity=record.quantity,
            area_m2=record.area_m2,
            notes=record.notes
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar registro de plantio: {str(e)}")

@router.get("/planting/project/{project_id}", response_model=PaginatedResponse)
async def get_project_planting_records(
    project_id: int = Path(..., description="ID do projeto"),
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    plant_type: Optional[str] = Query(None, description="Filtrar por tipo de planta"),
    species: Optional[str] = Query(None, description="Filtrar por espécie"),
    start_date: Optional[date] = Query(None, description="Data inicial de plantio"),
    end_date: Optional[date] = Query(None, description="Data final de plantio"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém todos os registros de plantio de um projeto específico, com opções de filtro e paginação.
    """
    try:
        # Verificar se o projeto existe e pertence ao usuário
        project = landscaping_db.get_project(project_id)
        if not project or project['user_id'] != current_user.id:
            raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
        
        filters = {
            "plant_type": plant_type,
            "species": species,
            "start_date": start_date,
            "end_date": end_date
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = landscaping_db.get_project_planting_records(project_id, filters, page, page_size)
        total_items = landscaping_db.count_project_planting_records(project_id, filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de plantio: {str(e)}")

# Endpoints para Dashboard
@router.get("/dashboard")
async def get_dashboard_summary(current_user: User = Depends(get_current_user)):
    """
    Obtém dados resumidos para o dashboard de paisagismo.
    """
    try:
        result = landscaping_db.get_dashboard_summary()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter resumo do dashboard: {str(e)}")

@router.get("/dashboard/project/{project_id}")
async def get_project_summary(
    project_id: int = Path(..., description="ID do projeto"),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém um resumo detalhado de um projeto específico.
    """
    try:
        # Verificar se o projeto existe e pertence ao usuário
        project = landscaping_db.get_project(project_id)
        if not project or project['user_id'] != current_user.id:
            raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado")
        
        result = landscaping_db.get_project_summary(project_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter resumo do projeto: {str(e)}")