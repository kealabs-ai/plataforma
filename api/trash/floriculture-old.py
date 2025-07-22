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
class FlowerCreate(BaseModel):
    species: str
    variety: Optional[str] = None
    planting_date: str
    area_m2: float
    greenhouse_id: Optional[int] = None
    expected_harvest_date: Optional[str] = None
    status: str = "active"
    notes: Optional[str] = None
    quantity: Optional[int] = None
    image_url: Optional[str] = None

class FlowerUpdate(BaseModel):
    species: Optional[str] = None
    variety: Optional[str] = None
    planting_date: Optional[str] = None
    area_m2: Optional[float] = None
    greenhouse_id: Optional[int] = None
    expected_harvest_date: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    quantity: Optional[int] = None
    image_url: Optional[str] = None

class FlowerResponse(BaseModel):
    id: int
    user_id: int
    species: str
    variety: Optional[str] = None
    planting_date: str
    area_m2: float
    greenhouse_id: Optional[int] = None
    expected_harvest_date: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    image_url: Optional[str] = None
    quantity: Optional[int] = None

class GreenhouseCreate(BaseModel):
    name: str
    area_m2: float
    type: str
    temperature_control: bool = False
    humidity_control: bool = False
    irrigation_system: bool = False
    location: Optional[str] = None
    notes: Optional[str] = None

class GreenhouseUpdate(BaseModel):
    name: Optional[str] = None
    area_m2: Optional[float] = None
    type: Optional[str] = None
    temperature_control: Optional[bool] = None
    humidity_control: Optional[bool] = None
    irrigation_system: Optional[bool] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class GreenhouseResponse(BaseModel):
    id: int
    user_id: int
    name: str
    area_m2: float
    type: str
    temperature_control: bool
    humidity_control: bool
    irrigation_system: bool
    location: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class SupplierCreate(BaseModel):
    name: str
    contact_person: str
    phone: str
    email: str
    products: str
    last_purchase: Optional[str] = None
    status: str = "Ativo"
    notes: Optional[str] = None

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    products: Optional[str] = None
    last_purchase: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class SupplierResponse(BaseModel):
    id: int
    user_id: int
    name: str
    contact_person: str
    phone: str
    email: str
    products: str
    last_purchase: Optional[str] = None
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
class FloricultureDB:
    def get_all_flower_cultivations(self, filters, page, page_size):
        # Implementação real seria conectar ao banco de dados
        # Retornando dados reais para demonstração
        return [
            {
                "id": 1,
                "user_id": 1,
                "species": "Rosa Vermelha",
                "variety": "Gallica",
                "planting_date": "2023-10-15",
                "area_m2": 25.5,
                "greenhouse_id": 1,
                "expected_harvest_date": "2024-01-15",
                "status": "active",
                "notes": "Rosa vermelha tradicional, perfeita para jardins e arranjos.",
                "created_at": "2023-10-15T10:00:00",
                "updated_at": "2023-10-15T10:00:00",
                "image_url": "https://images.unsplash.com/photo-1559563362-c667ba5f5480",
                "quantity": 50
            }
        ]
    
    def count_flower_cultivations(self, filters):
        return 1
    
    def get_flower_cultivation(self, flower_id):
        return {
            "id": flower_id,
            "user_id": 1,
            "species": "Rosa Vermelha",
            "variety": "Gallica",
            "planting_date": "2023-10-15",
            "area_m2": 25.5,
            "greenhouse_id": 1,
            "expected_harvest_date": "2024-01-15",
            "status": "active",
            "notes": "Rosa vermelha tradicional, perfeita para jardins e arranjos.",
            "created_at": "2023-10-15T10:00:00",
            "updated_at": "2023-10-15T10:00:00",
            "image_url": "https://images.unsplash.com/photo-1559563362-c667ba5f5480",
            "quantity": 50
        }
    
    def create_flower_cultivation(self, species, variety, planting_date, area_m2, 
                                greenhouse_id=None, expected_harvest_date=None, status="active", 
                                notes=None, quantity=None, image_url=None):
        now = datetime.now().isoformat()
        return {
            "id": 1,
            "user_id": 1,
            "species": species,
            "variety": variety,
            "planting_date": planting_date,
            "area_m2": area_m2,
            "greenhouse_id": greenhouse_id,
            "expected_harvest_date": expected_harvest_date,
            "status": status,
            "notes": notes,
            "created_at": now,
            "updated_at": now,
            "image_url": image_url,
            "quantity": quantity
        }
    
    def update_flower_cultivation(self, flower_id, update_data):
        flower = self.get_flower_cultivation(flower_id)
        if flower:
            for key, value in update_data.items():
                flower[key] = value
            flower["updated_at"] = datetime.now().isoformat()
            return flower
        return None
    
    def delete_flower_cultivation(self, flower_id):
        flower = self.get_flower_cultivation(flower_id)
        return flower is not None
    
    def get_all_greenhouses(self, filters, page, page_size):
        return [
            {
                "id": 1,
                "user_id": 1,
                "name": "Estufa Principal",
                "area_m2": 100.0,
                "type": "Vidro",
                "temperature_control": True,
                "humidity_control": True,
                "irrigation_system": True,
                "location": "Setor Norte",
                "notes": "Estufa principal para cultivo de flores exóticas",
                "created_at": "2023-09-01T10:00:00",
                "updated_at": "2023-09-01T10:00:00"
            }
        ]
    
    def count_greenhouses(self, filters):
        return 1
    
    def get_greenhouse(self, greenhouse_id):
        return {
            "id": greenhouse_id,
            "user_id": 1,
            "name": "Estufa Principal",
            "area_m2": 100.0,
            "type": "Vidro",
            "temperature_control": True,
            "humidity_control": True,
            "irrigation_system": True,
            "location": "Setor Norte",
            "notes": "Estufa principal para cultivo de flores exóticas",
            "created_at": "2023-09-01T10:00:00",
            "updated_at": "2023-09-01T10:00:00"
        }
    
    def create_greenhouse(self, name, area_m2, type, temperature_control=False,
                        humidity_control=False, irrigation_system=False, location=None, notes=None):
        now = datetime.now().isoformat()
        return {
            "id": 1,
            "user_id": 1,
            "name": name,
            "area_m2": area_m2,
            "type": type,
            "temperature_control": temperature_control,
            "humidity_control": humidity_control,
            "irrigation_system": irrigation_system,
            "location": location,
            "notes": notes,
            "created_at": now,
            "updated_at": now
        }
    
    def get_all_suppliers(self, filters, page, page_size):
        return [
            {
                "id": 1,
                "user_id": 1,
                "name": "Flores & Cia",
                "contact_person": "João Silva",
                "phone": "(11) 98765-4321",
                "email": "contato@floresecia.com.br",
                "products": "Flores, Sementes, Mudas",
                "last_purchase": "2023-08-15",
                "status": "Ativo",
                "notes": "Fornecedor principal de sementes",
                "created_at": "2023-08-01T10:00:00",
                "updated_at": "2023-08-01T10:00:00"
            }
        ]
    
    def count_suppliers(self, filters):
        return 1
    
    def get_supplier(self, supplier_id):
        return {
            "id": supplier_id,
            "user_id": 1,
            "name": "Flores & Cia",
            "contact_person": "João Silva",
            "phone": "(11) 98765-4321",
            "email": "contato@floresecia.com.br",
            "products": "Flores, Sementes, Mudas",
            "last_purchase": "2023-08-15",
            "status": "Ativo",
            "notes": "Fornecedor principal de sementes",
            "created_at": "2023-08-01T10:00:00",
            "updated_at": "2023-08-01T10:00:00"
        }
    
    def create_supplier(self, name, contact_person, phone, email, products,
                      last_purchase=None, status="Ativo", notes=None):
        now = datetime.now().isoformat()
        return {
            "id": 1,
            "user_id": 1,
            "name": name,
            "contact_person": contact_person,
            "phone": phone,
            "email": email,
            "products": products,
            "last_purchase": last_purchase,
            "status": status,
            "notes": notes,
            "created_at": now,
            "updated_at": now
        }

# Instância do banco de dados
floriculture_db = FloricultureDB()

router = APIRouter(prefix="/floriculture/endpoints", tags=["Floricultura"])

# Endpoints para Cultivos de Flores
@router.get("/flowers", response_model=PaginatedResponse)
async def get_all_flowers(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    species: Optional[str] = Query(None, description="Filtrar por espécie"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    greenhouse_id: Optional[int] = Query(None, description="Filtrar por estufa")
):
    """
    Obtém todos os registros de cultivo de flores, com opções de filtro e paginação.
    """
    try:
        filters = {
            "species": species,
            "status": status,
            "greenhouse_id": greenhouse_id,
            "user_id": 1  # Usuário fixo para simplificar
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = floriculture_db.get_all_flower_cultivations(filters, page, page_size)
        total_items = floriculture_db.count_flower_cultivations(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter cultivos de flores: {str(e)}")

@router.get("/flowers/{flower_id}", response_model=FlowerResponse)
async def get_flower(
    flower_id: int = Path(..., description="ID do cultivo")
):
    """
    Obtém um registro específico de cultivo de flores pelo ID.
    """
    try:
        flower = floriculture_db.get_flower_cultivation(flower_id)
        
        if not flower:
            raise HTTPException(status_code=404, detail=f"Cultivo com ID {flower_id} não encontrado")
        
        return flower
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter cultivo: {str(e)}")

@router.post("/flowers", response_model=FlowerResponse)
async def create_flower(
    flower: FlowerCreate = Body(...)
):
    """
    Cria um novo registro de cultivo de flores.
    """
    try:
        result = floriculture_db.create_flower_cultivation(
            species=flower.species,
            variety=flower.variety,
            planting_date=flower.planting_date,
            area_m2=flower.area_m2,
            greenhouse_id=flower.greenhouse_id,
            expected_harvest_date=flower.expected_harvest_date,
            status=flower.status,
            notes=flower.notes,
            quantity=flower.quantity,
            image_url=flower.image_url
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar cultivo de flores")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cultivo de flores: {str(e)}")

# Endpoints para Estufas
@router.get("/greenhouses", response_model=PaginatedResponse)
async def get_all_greenhouses(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    type: Optional[str] = Query(None, description="Filtrar por tipo")
):
    """
    Obtém todas as estufas, com opções de filtro e paginação.
    """
    try:
        filters = {
            "type": type,
            "user_id": 1  # Usuário fixo para simplificar
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = floriculture_db.get_all_greenhouses(filters, page, page_size)
        total_items = floriculture_db.count_greenhouses(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estufas: {str(e)}")

# Endpoints para Fornecedores
@router.get("/suppliers", response_model=PaginatedResponse)
async def get_all_suppliers(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    name: Optional[str] = Query(None, description="Filtrar por nome")
):
    """
    Obtém todos os fornecedores, com opções de filtro e paginação.
    """
    try:
        filters = {
            "status": status,
            "name": name,
            "user_id": 1  # Usuário fixo para simplificar
        }
        
        # Remover filtros vazios
        filters = {k: v for k, v in filters.items() if v is not None}
        
        items = floriculture_db.get_all_suppliers(filters, page, page_size)
        total_items = floriculture_db.count_suppliers(filters)
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