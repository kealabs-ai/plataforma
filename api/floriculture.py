from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from pydantic import BaseModel, validator, Field
from database_queries.floriculture_database_query import *

router = APIRouter(
    prefix="/api/floriculture",
    tags=["Floriculture"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class FlowerCultivationBase(BaseModel):
    user_id: int
    species: str
    variety: Optional[str] = None
    planting_date: date
    quantity: Optional[int] = None
    area_m2: float
    greenhouse_id: Optional[int] = None
    expected_harvest_date: Optional[date] = None
    status: str = "active"
    notes: Optional[str] = None
    image_url: Optional[str] = None

class FlowerCultivationCreate(FlowerCultivationBase):
    pass

class FlowerCultivationUpdate(BaseModel):
    species: Optional[str] = None
    variety: Optional[str] = None
    quantity: Optional[int] = None
    area_m2: Optional[float] = None
    greenhouse_id: Optional[int] = None
    expected_harvest_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    image_url: Optional[str] = None

class FlowerCultivationResponse(FlowerCultivationBase):
    id: int

class GreenhouseBase(BaseModel):
    user_id: int
    name: str
    area_m2: float
    type: str
    temperature_control: bool = False
    humidity_control: bool = False
    irrigation_system: bool = False
    location: Optional[str] = None
    notes: Optional[str] = None

class GreenhouseCreate(GreenhouseBase):
    pass

class GreenhouseUpdate(BaseModel):
    name: Optional[str] = None
    area_m2: Optional[float] = None
    type: Optional[str] = None
    temperature_control: Optional[bool] = None
    humidity_control: Optional[bool] = None
    irrigation_system: Optional[bool] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class GreenhouseResponse(GreenhouseBase):
    id: int

class SupplierBase(BaseModel):
    user_id: int
    name: str
    contact_person: str
    phone: str
    email: str
    products: str
    last_purchase: Optional[date] = None
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
    last_purchase: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class SupplierResponse(SupplierBase):
    id: int

class PaginatedResponse(BaseModel):
    items: List[Any]
    page: int
    page_size: int
    total_items: int
    total_pages: int

# --- FLOWER CULTIVATION ENDPOINTS ---

@router.post("/cultivation", response_model=FlowerCultivationResponse)
async def create_cultivation(cultivation: FlowerCultivationCreate = Body(...)):
    """
    Cria um novo registro de cultivo de flores.
    """
    try:
        result = create_flower_cultivation(
            user_id=cultivation.user_id,
            species=cultivation.species,
            variety=cultivation.variety,
            planting_date=cultivation.planting_date,
            quantity=cultivation.quantity,
            area_m2=cultivation.area_m2,
            greenhouse_id=cultivation.greenhouse_id,
            expected_harvest_date=cultivation.expected_harvest_date,
            status=cultivation.status,
            notes=cultivation.notes,
            image_url=cultivation.image_url
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar cultivo de flores")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cultivo de flores: {str(e)}")

@router.get("/cultivation", response_model=PaginatedResponse)
async def get_all_cultivations(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    status: Optional[str] = Query(None, description="Status do cultivo"),
    species: Optional[str] = Query(None, description="Espécie de flor")
):
    """
    Obtém todos os registros de cultivo de flores com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "status": status,
            "species": species
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_flower_cultivations(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_flower_cultivations(filters, page, page_size)
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter cultivos de flores: {str(e)}")

@router.get("/cultivation/{cultivation_id}", response_model=FlowerCultivationResponse)
async def get_cultivation(cultivation_id: int = Path(..., description="ID do cultivo")):
    """
    Obtém um registro específico de cultivo de flores pelo ID.
    """
    try:
        result = get_flower_cultivation(cultivation_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Cultivo com ID {cultivation_id} não encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter cultivo: {str(e)}")

# --- GREENHOUSE ENDPOINTS ---

@router.post("/greenhouse", response_model=GreenhouseResponse)
async def create_greenhouse_endpoint(greenhouse: GreenhouseCreate = Body(...)):
    """
    Cria uma nova estufa.
    """
    try:
        result = create_greenhouse(
            user_id=greenhouse.user_id,
            name=greenhouse.name,
            area_m2=greenhouse.area_m2,
            type=greenhouse.type,
            temperature_control=greenhouse.temperature_control,
            humidity_control=greenhouse.humidity_control,
            irrigation_system=greenhouse.irrigation_system,
            location=greenhouse.location,
            notes=greenhouse.notes
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar estufa")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar estufa: {str(e)}")

@router.get("/greenhouse", response_model=PaginatedResponse)
async def get_all_greenhouses_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    type: Optional[str] = Query(None, description="Tipo de estufa")
):
    """
    Obtém todas as estufas com filtros e paginação.
    """
    try:
        filters = {
            "user_id": user_id,
            "type": type
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = count_greenhouses(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = get_all_greenhouses(filters, page, page_size)
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estufas: {str(e)}")

@router.get("/greenhouse/{greenhouse_id}", response_model=GreenhouseResponse)
async def get_greenhouse_endpoint(greenhouse_id: int = Path(..., description="ID da estufa")):
    """
    Obtém uma estufa específica pelo ID.
    """
    try:
        result = get_greenhouse(greenhouse_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Estufa com ID {greenhouse_id} não encontrada")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estufa: {str(e)}")

@router.put("/greenhouse/{greenhouse_id}", response_model=GreenhouseResponse)
async def update_greenhouse_endpoint(
    greenhouse_id: int = Path(..., description="ID da estufa"),
    user_id: int = Query(..., description="ID do usuário"),
    greenhouse_data: GreenhouseUpdate = Body(...)
):
    """
    Atualiza uma estufa.
    """
    try:
        update_data = {k: v for k, v in greenhouse_data.dict().items() if v is not None}
        result = update_greenhouse(greenhouse_id, user_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Estufa com ID {greenhouse_id} não encontrada ou não pertence ao usuário")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar estufa: {str(e)}")

@router.delete("/greenhouse/{greenhouse_id}")
async def delete_greenhouse_endpoint(
    greenhouse_id: int = Path(..., description="ID da estufa"),
    user_id: int = Query(..., description="ID do usuário")
):
    """
    Remove uma estufa.
    """
    try:
        success = delete_greenhouse(greenhouse_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Estufa com ID {greenhouse_id} não encontrada ou não pertence ao usuário")
        return {"message": f"Estufa com ID {greenhouse_id} removida com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover estufa: {str(e)}")

# --- SUPPLIER ENDPOINTS ---

@router.post("/supplier", response_model=SupplierResponse)
async def create_supplier_endpoint(supplier: SupplierCreate = Body(...)):
    """
    Cria um novo fornecedor.
    """
    try:
        result = create_supplier(
            user_id=supplier.user_id,
            name=supplier.name,
            contact_person=supplier.contact_person,
            phone=supplier.phone,
            email=supplier.email,
            products=supplier.products,
            last_purchase=supplier.last_purchase,
            status=supplier.status,
            notes=supplier.notes
        )
        if not result:
            raise HTTPException(status_code=500, detail="Erro ao criar fornecedor")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar fornecedor: {str(e)}")

@router.get("/supplier", response_model=PaginatedResponse)
async def get_all_suppliers_endpoint(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    user_id: Optional[int] = Query(None, description="ID do usuário"),
    status: Optional[str] = Query(None, description="Status do fornecedor"),
    name: Optional[str] = Query(None, description="Nome do fornecedor")
):
    """
    Obtém todos os fornecedores com filtros e paginação.
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
        raise HTTPException(status_code=500, detail=f"Erro ao obter fornecedores: {str(e)}")

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

@router.put("/supplier/{supplier_id}", response_model=SupplierResponse)
async def update_supplier_endpoint(
    supplier_id: int = Path(..., description="ID do fornecedor"),
    user_id: int = Query(..., description="ID do usuário"),
    supplier_data: SupplierUpdate = Body(...)
):
    """
    Atualiza um fornecedor.
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
    Remove um fornecedor.
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