# main.py
from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date

# Importa as funções de operações de banco de dados
from data.floriculture_db import (
    create_flower_cultivation, get_all_flower_cultivations, count_flower_cultivations, get_flower_cultivation,
   # update_flower_cultivation, delete_flower_cultivation, # Funções de CRUD Flower Cultivation agora completas
    create_greenhouse, get_all_greenhouses, count_greenhouses, get_greenhouse, update_greenhouse, delete_greenhouse,
    create_supplier, get_all_suppliers, count_suppliers, get_supplier, update_supplier, delete_supplier
)

app = FastAPI(
    title="API de Floricultura",
    description="API para gerenciar cultivos de flores, estufas e fornecedores."
)

# --- Schemas Pydantic para validação de dados ---

class FlowerCultivationCreate(BaseModel):
    user_id: int
    species: str = Field(..., example="Rosa")
    variety: Optional[str] = Field(None, example="Vermelha")
    planting_date: date = Field(..., example="2024-01-15")
    quantity: Optional[int] = Field(None, example=100)
    area_m2: float = Field(..., example=50.5)
    greenhouse_id: Optional[int] = Field(None, example=1)
    expected_harvest_date: Optional[date] = Field(None, example="2024-05-20")
    status: str = Field("active", example="active")
    notes: Optional[str] = Field(None, example="Primeiro plantio da estação.")
    image_url: Optional[str] = Field(None, example="http://example.com/rose.jpg")

class FlowerCultivationUpdate(BaseModel):
    species: Optional[str] = None
    variety: Optional[str] = None
    planting_date: Optional[date] = None
    quantity: Optional[int] = None
    area_m2: Optional[float] = None
    greenhouse_id: Optional[int] = None
    expected_harvest_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None

class FlowerCultivationResponse(FlowerCultivationCreate):
    id: int
    # created_at: date # Descomente se seu DB realmente retornar este campo

    class Config:
        from_attributes = True

class GreenhouseCreate(BaseModel):
    user_id: int
    name: str = Field(..., example="Estufa Principal")
    area_m2: float = Field(..., example=120.0)
    type: str = Field(..., example="Vidro")
    temperature_control: bool = Field(False, example=True)
    humidity_control: bool = Field(False, example=True)
    irrigation_system: bool = Field(False, example=True)
    location: Optional[str] = Field(None, example="Setor A")
    notes: Optional[str] = Field(None, example="Bem ventilada.")

class GreenhouseUpdate(BaseModel):
    name: Optional[str] = None
    area_m2: Optional[float] = None
    type: Optional[str] = None
    temperature_control: Optional[bool] = None
    humidity_control: Optional[bool] = None
    irrigation_system: Optional[bool] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class GreenhouseResponse(GreenhouseCreate):
    id: int

    class Config:
        from_attributes = True

class SupplierCreate(BaseModel):
    user_id: int
    name: str = Field(..., example="Flores do Campo Ltda.")
    contact_person: str = Field(..., example="João Silva")
    phone: str = Field(..., example="5531998765432")
    email: str = Field(..., example="contato@floresdocampo.com")
    products: str = Field(..., example="Sementes, Fertilizantes")
    last_purchase: Optional[date] = Field(None, example="2024-03-10")
    status: str = Field("Ativo", example="Ativo")
    notes: Optional[str] = Field(None, example="Excelente qualidade e prazos.")

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    products: Optional[str] = None
    last_purchase: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class SupplierResponse(SupplierCreate):
    id: int

    class Config:
        from_attributes = True

router = APIRouter(
    prefix="/floriculture",
    tags=["Floriculture"],
)

# --- Dependências (para simular autenticação ou contexto de usuário) ---
def get_current_user_id(user_id: int = Query(..., description="ID do usuário para autenticação/autorização")) -> int:
    """
    Retorna o ID do usuário atual. Em um sistema real, isso seria obtido
    de um token de autenticação (JWT, OAuth2, etc.).
    """
    return user_id

# --- Endpoints de Cultivo de Flores ---

@app.post("/flower_cultivations/", response_model=FlowerCultivationResponse, status_code=201)
async def create_flower_cultivation_endpoint(
    cultivation: FlowerCultivationCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Cria um novo registro de cultivo de flores.
    """
    if cultivation.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a criar cultivos para outro usuário.")

    new_cultivation = create_flower_cultivation(**cultivation.model_dump())
    if not new_cultivation:
        raise HTTPException(status_code=500, detail="Erro ao criar cultivo de flores.")
    return new_cultivation

@app.get("/flower_cultivations/", response_model=List[FlowerCultivationResponse])
async def get_all_flower_cultivations_endpoint(
    user_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    species: Optional[str] = Query(None, description="Filtrar por espécie"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Obtém todos os registros de cultivo de flores com filtros e paginação.
    Um usuário só pode ver seus próprios cultivos.
    """
    filters = {"user_id": current_user_id} # Sempre filtra pelo usuário logado

    if user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a ver cultivos de outros usuários.")
    if species:
        filters["species"] = species
    if status:
        filters["status"] = status

    cultivations = get_all_flower_cultivations(filters, page, page_size)
    return cultivations

@app.get("/flower_cultivations/count/", response_model=int)
async def count_flower_cultivations_endpoint(
    user_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    species: Optional[str] = Query(None, description="Filtrar por espécie"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Conta o total de registros de cultivo de flores com filtros.
    Um usuário só pode contar seus próprios cultivos.
    """
    filters = {"user_id": current_user_id} # Sempre filtra pelo usuário logado

    if user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a contar cultivos de outros usuários.")
    if species:
        filters["species"] = species
    if status:
        filters["status"] = status

    count = count_flower_cultivations(filters)
    return count

@app.get("/flower_cultivations/{flower_id}", response_model=FlowerCultivationResponse)
async def get_flower_cultivation_endpoint(
    flower_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Obtém um registro específico de cultivo de flores pelo ID.
    O usuário só pode acessar seus próprios cultivos.
    """
    cultivation = get_flower_cultivation(flower_id)
    if not cultivation:
        raise HTTPException(status_code=404, detail="Cultivo de flores não encontrado.")
    if cultivation["user_id"] != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a acessar este cultivo de flores.")
    return cultivation


# --- Endpoints de Estufas ---

@app.post("/greenhouses/", response_model=GreenhouseResponse, status_code=201)
async def create_greenhouse_endpoint(
    greenhouse: GreenhouseCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Cria uma nova estufa.
    """
    if greenhouse.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a criar estufas para outro usuário.")

    new_greenhouse = create_greenhouse(**greenhouse.model_dump())
    if not new_greenhouse:
        raise HTTPException(status_code=500, detail="Erro ao criar estufa.")
    return new_greenhouse

@app.get("/greenhouses/", response_model=List[GreenhouseResponse])
async def get_all_greenhouses_endpoint(
    user_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    type: Optional[str] = Query(None, description="Filtrar por tipo de estufa"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Obtém todas as estufas com filtros e paginação.
    Um usuário só pode ver suas próprias estufas.
    """
    filters = {"user_id": current_user_id} # Sempre filtra pelo usuário logado

    if user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a ver estufas de outros usuários.")
    if type:
        filters["type"] = type
    
    greenhouses = get_all_greenhouses(filters, page, page_size)
    return greenhouses

@app.get("/greenhouses/count/", response_model=int)
async def count_greenhouses_endpoint(
    user_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    type: Optional[str] = Query(None, description="Filtrar por tipo de estufa"),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Conta o total de estufas com filtros.
    Um usuário só pode contar suas próprias estufas.
    """
    filters = {"user_id": current_user_id} # Sempre filtra pelo usuário logado

    if user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a contar estufas de outros usuários.")
    if type:
        filters["type"] = type

    count = count_greenhouses(filters)
    return count

@app.get("/greenhouses/{greenhouse_id}", response_model=GreenhouseResponse)
async def get_greenhouse_endpoint(
    greenhouse_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Obtém uma estufa específica pelo ID.
    O usuário só pode acessar suas próprias estufas.
    """
    greenhouse = get_greenhouse(greenhouse_id)
    if not greenhouse:
        raise HTTPException(status_code=404, detail="Estufa não encontrada.")
    if greenhouse["user_id"] != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a acessar esta estufa.")
    return greenhouse

@app.put("/greenhouses/{greenhouse_id}", response_model=GreenhouseResponse)
async def update_greenhouse_endpoint(
    greenhouse_id: int,
    update_data: GreenhouseUpdate,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Atualiza uma estufa.
    O usuário só pode atualizar suas próprias estufas.
    """
    data_to_update = update_data.model_dump(exclude_unset=True)
    
    updated_greenhouse = update_greenhouse(greenhouse_id, current_user_id, data_to_update)
    if not updated_greenhouse:
        if get_greenhouse(greenhouse_id):
            raise HTTPException(status_code=403, detail="Não autorizado a atualizar esta estufa.")
        raise HTTPException(status_code=404, detail="Estufa não encontrada ou não foi possível atualizar.")
    return updated_greenhouse

@app.delete("/greenhouses/{greenhouse_id}", status_code=204)
async def delete_greenhouse_endpoint(
    greenhouse_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Remove uma estufa.
    O usuário só pode deletar suas próprias estufas.
    """
    if not delete_greenhouse(greenhouse_id, current_user_id):
        if get_greenhouse(greenhouse_id):
            raise HTTPException(status_code=403, detail="Não autorizado a deletar esta estufa.")
        raise HTTPException(status_code=404, detail="Estufa não encontrada ou não foi possível deletar.")
    return

# --- Endpoints de Fornecedores ---

@app.post("/suppliers/", response_model=SupplierResponse, status_code=201)
async def create_supplier_endpoint(
    supplier: SupplierCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Cria um novo fornecedor.
    """
    if supplier.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a criar fornecedores para outro usuário.")

    new_supplier = create_supplier(**supplier.model_dump())
    if not new_supplier:
        raise HTTPException(status_code=500, detail="Erro ao criar fornecedor.")
    return new_supplier

@app.get("/suppliers/", response_model=List[SupplierResponse])
async def get_all_suppliers_endpoint(
    user_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    name: Optional[str] = Query(None, description="Filtrar por nome (busca parcial)"),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Obtém todos os fornecedores com filtros e paginação.
    Um usuário só pode ver seus próprios fornecedores.
    """
    filters = {"user_id": current_user_id} # Sempre filtra pelo usuário logado

    if user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a ver fornecedores de outros usuários.")
    if status:
        filters["status"] = status
    if name:
        filters["name"] = name
    
    suppliers = get_all_suppliers(filters, page, page_size)
    return suppliers

@app.get("/suppliers/count/", response_model=int)
async def count_suppliers_endpoint(
    user_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    name: Optional[str] = Query(None, description="Filtrar por nome (busca parcial)"),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Conta o total de fornecedores com filtros.
    Um usuário só pode contar seus próprios fornecedores.
    """
    filters = {"user_id": current_user_id} # Sempre filtra pelo usuário logado

    if user_id and user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a contar fornecedores de outros usuários.")
    if status:
        filters["status"] = status
    if name:
        filters["name"] = name

    count = count_suppliers(filters)
    return count

@app.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier_endpoint(
    supplier_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Obtém um fornecedor específico pelo ID.
    O usuário só pode acessar seus próprios fornecedores.
    """
    supplier = get_supplier(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado.")
    if supplier["user_id"] != current_user_id:
        raise HTTPException(status_code=403, detail="Não autorizado a acessar este fornecedor.")
    return supplier

@app.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier_endpoint(
    supplier_id: int,
    update_data: SupplierUpdate,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Atualiza um fornecedor.
    O usuário só pode atualizar seus próprios fornecedores.
    """
    data_to_update = update_data.model_dump(exclude_unset=True)

    updated_supplier = update_supplier(supplier_id, current_user_id, data_to_update)
    if not updated_supplier:
        if get_supplier(supplier_id):
            raise HTTPException(status_code=403, detail="Não autorizado a atualizar este fornecedor.")
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado ou não foi possível atualizar.")
    return updated_supplier

@app.delete("/suppliers/{supplier_id}", status_code=204)
async def delete_supplier_endpoint(
    supplier_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Remove um fornecedor.
    O usuário só pode deletar seus próprios fornecedores.
    """
    if not delete_supplier(supplier_id, current_user_id):
        if get_supplier(supplier_id):
            raise HTTPException(status_code=403, detail="Não autorizado a deletar este fornecedor.")
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado ou não foi possível deletar.")
    return