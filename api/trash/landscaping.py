from fastapi import APIRouter, HTTPException, Path, Query, Body
from typing import Optional, List
from pydantic import BaseModel
import sys
import os
from datetime import datetime

# Adiciona o diretório raiz ao path para importações relativas
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Definições de modelos diretamente no arquivo
class ProjectCreate(BaseModel):
    name: str
    client_name: str
    area_m2: float
    location: str
    start_date: str
    end_date: Optional[str] = None
    budget: Optional[float] = None
    status: str = "planejamento"
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    client_name: str
    area_m2: float
    location: str
    start_date: str
    end_date: Optional[str] = None
    budget: Optional[float] = None
    status: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class SupplierCreate(BaseModel):
    name: str
    contact_person: str
    phone: str
    email: str
    products: str
    last_contract: Optional[str] = None
    status: str = "Ativo"
    notes: Optional[str] = None

class SupplierResponse(BaseModel):
    id: int
    user_id: int
    name: str
    contact_person: str
    phone: str
    email: str
    products: str
    last_contract: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    page: int
    page_size: int
    total_items: int
    total_pages: int

# Classe para simular o acesso ao banco de dados
class LandscapingDB:
    def get_all_projects(self, filters, page, page_size):
        # Implementação real seria conectar ao banco de dados
        # Retornando dados reais para demonstração
        return [
            {
                "id": 1,
                "user_id": 1,
                "name": "Jardim Residencial Vila Verde",
                "client_name": "Maria Silva",
                "start_date": "2023-05-15",
                "end_date": "2023-06-30",
                "area_m2": 120,
                "budget": 8500.00,
                "status": "concluído",
                "location": "Rua das Flores, 123",
                "description": "Projeto de jardim residencial com foco em plantas nativas e sustentabilidade.",
                "created_at": "2023-05-01T10:00:00",
                "updated_at": "2023-06-30T15:00:00"
            },
            {
                "id": 2,
                "user_id": 1,
                "name": "Praça Empresarial Tech Park",
                "client_name": "Tech Innovations LTDA",
                "start_date": "2023-07-10",
                "end_date": "2023-09-15",
                "area_m2": 450,
                "budget": 32000.00,
                "status": "em_andamento",
                "location": "Av. Tecnologia, 500",
                "description": "Revitalização da praça central do parque empresarial com conceito moderno e sustentável.",
                "created_at": "2023-07-01T10:00:00",
                "updated_at": "2023-08-15T15:00:00"
            }
        ]
    
    def count_projects(self, filters):
        return 2
    
    def get_project(self, project_id):
        projects = self.get_all_projects({}, 1, 10)
        for project in projects:
            if project["id"] == project_id:
                return project
        return None
    
    def create_project(self, name, client_name, area_m2, location, start_date,
                     end_date=None, budget=None, status="planejamento", description=None):
        now = datetime.now().isoformat()
        return {
            "id": 3,
            "user_id": 1,
            "name": name,
            "client_name": client_name,
            "start_date": start_date,
            "end_date": end_date,
            "area_m2": area_m2,
            "budget": budget,
            "status": status,
            "location": location,
            "description": description,
            "created_at": now,
            "updated_at": now
        }
    
    def update_project(self, project_id, update_data):
        project = self.get_project(project_id)
        if project:
            for key, value in update_data.items():
                project[key] = value
            project["updated_at"] = datetime.now().isoformat()
            return project
        return None
    
    def delete_project(self, project_id):
        project = self.get_project(project_id)
        return project is not None
    
    def get_all_suppliers(self, filters, page, page_size):
        return [
            {
                "id": 1,
                "user_id": 1,
                "name": "Pedras & Jardins",
                "contact_person": "Roberto Almeida",
                "phone": "(11) 99876-5432",
                "email": "contato@pedrasejardins.com.br",
                "products": "Pedras decorativas, Cascalho, Areia",
                "last_contract": "2023-10-15",
                "status": "Ativo",
                "notes": "Fornecedor de materiais para pavimentação",
                "created_at": "2023-09-01T10:00:00",
                "updated_at": "2023-09-01T10:00:00"
            },
            {
                "id": 2,
                "user_id": 1,
                "name": "Árvores Brasil",
                "contact_person": "Ana Ferreira",
                "phone": "(11) 98765-1234",
                "email": "vendas@arvoresbrasil.com.br",
                "products": "Árvores, Arbustos, Palmeiras",
                "last_contract": "2023-11-20",
                "status": "Ativo",
                "notes": "Fornecedor especializado em árvores nativas",
                "created_at": "2023-09-15T10:00:00",
                "updated_at": "2023-09-15T10:00:00"
            }
        ]
    
    def count_suppliers(self, filters):
        return 2
    
    def get_supplier(self, supplier_id):
        suppliers = self.get_all_suppliers({}, 1, 10)
        for supplier in suppliers:
            if supplier["id"] == supplier_id:
                return supplier
        return None
    
    def create_supplier(self, name, contact_person, phone, email, products,
                      last_contract=None, status="Ativo", notes=None):
        now = datetime.now().isoformat()
        return {
            "id": 3,
            "user_id": 1,
            "name": name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "products": products,
            "last_contract": last_contract,
            "status": status,
            "notes": notes,
            "created_at": now,
            "updated_at": now
        }

# Instância do banco de dados
landscaping_db = LandscapingDB()

router = APIRouter(prefix="/landscaping/endpoints", tags=["Paisagismo"])

# Endpoints para Projetos
@router.get("/projects", response_model=PaginatedResponse)
async def get_all_projects(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    client_name: Optional[str] = Query(None, description="Filtrar por cliente")
):
    """
    Obtém todos os projetos de paisagismo, com opções de filtro e paginação.
    """
    try:
        filters = {
            "status": status,
            "client_name": client_name,
            "user_id": 1  # Usuário fixo para simplificar
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
    project_id: int = Path(..., description="ID do projeto")
):
    """
    Obtém um projeto específico pelo ID.
    """
    try:
        project = landscaping_db.get_project(project_id)
        
        if not project:
            raise HTTPException(status_code=404, detail=f"Projeto com ID {project_id} não encontrado")
        
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter projeto: {str(e)}")

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate = Body(...)
):
    """
    Cria um novo projeto de paisagismo.
    """
    try:
        result = landscaping_db.create_project(
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
            raise HTTPException(status_code=500, detail="Erro ao criar projeto")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar projeto: {str(e)}")

# Endpoints para Fornecedores
@router.get("/suppliers", response_model=PaginatedResponse)
async def get_all_suppliers(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    name: Optional[str] = Query(None, description="Filtrar por nome")
):
    """
    Obtém todos os fornecedores de paisagismo, com opções de filtro e paginação.
    """
    try:
        filters = {
            "status": status,
            "name": name,
            "user_id": 1  # Usuário fixo para simplificar
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

@router.post("/suppliers", response_model=SupplierResponse)
async def create_supplier(
    supplier: SupplierCreate = Body(...)
):
    """
    Cria um novo fornecedor de paisagismo.
    """
    try:
        result = landscaping_db.create_supplier(
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