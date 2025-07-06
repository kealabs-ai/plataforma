from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from pydantic import BaseModel, validator, Field
from backend.beef_cattle_database import beef_cattle_db

router = APIRouter(
    prefix="/api/beef_cattle",
    tags=["Beef Cattle"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class BeefCattleBase(BaseModel):
    official_id: str
    name: Optional[str] = None
    birth_date: date
    breed: Optional[str] = None
    gender: str
    entry_date: date
    entry_weight: float
    current_weight: Optional[float] = None
    target_weight: Optional[float] = None
    status: str = "Em Engorda"
    expected_finish_date: Optional[date] = None
    notes: Optional[str] = None

class BeefCattleCreate(BeefCattleBase):
    pass

class BeefCattleUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    current_weight: Optional[float] = None
    target_weight: Optional[float] = None
    status: Optional[str] = None
    expected_finish_date: Optional[date] = None
    notes: Optional[str] = None

class BeefCattleResponse(BeefCattleBase):
    id: int
    created_at: datetime
    updated_at: datetime

class WeightRecordBase(BaseModel):
    cattle_id: int
    weight_date: date
    weight: float
    notes: Optional[str] = None
    user_id: Optional[int] = None

class WeightRecordCreate(WeightRecordBase):
    pass

class WeightRecordResponse(WeightRecordBase):
    id: int
    created_at: datetime

class FeedingRecordBase(BaseModel):
    cattle_id: int
    feeding_date: date
    feed_type: str
    quantity: float
    unit: str
    notes: Optional[str] = None
    user_id: Optional[int] = None

class FeedingRecordCreate(FeedingRecordBase):
    pass

class FeedingRecordResponse(FeedingRecordBase):
    id: int
    created_at: datetime

class HealthRecordBase(BaseModel):
    cattle_id: int
    record_date: date
    record_type: str
    description: str
    medicine: Optional[str] = None
    dosage: Optional[str] = None
    notes: Optional[str] = None
    user_id: Optional[int] = None

class HealthRecordCreate(HealthRecordBase):
    pass

class HealthRecordResponse(HealthRecordBase):
    id: int
    created_at: datetime

class SaleRecordBase(BaseModel):
    cattle_id: int
    sale_date: date
    final_weight: float
    price_per_kg: float
    total_value: float
    buyer: Optional[str] = None
    notes: Optional[str] = None
    user_id: Optional[int] = None

class SaleRecordCreate(SaleRecordBase):
    pass

class SaleRecordResponse(SaleRecordBase):
    id: int
    created_at: datetime

class FilterParams(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    breed: Optional[str] = None
    min_weight: Optional[float] = None
    max_weight: Optional[float] = None
    
    @validator('start_date', 'end_date', pre=True)
    def validate_date(cls, value):
        if not value:
            return None
            
        if isinstance(value, date):
            return value
            
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError as e:
            raise ValueError(f"Formato de data inválido. Use o formato YYYY-MM-DD.")
        
        return value

# --- Mova as rotas dinâmicas para o final do arquivo ---

# Beef Cattle CRUD endpoints
@router.post("/", response_model=BeefCattleResponse)
async def create_beef_cattle(cattle: BeefCattleCreate = Body(...)):
    """
    Cria um novo registro de boi para engorda.
    """
    try:
        result = beef_cattle_db.create_beef_cattle(cattle.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar registro: {str(e)}")

class PaginatedResponse(BaseModel):
    items: List[Any]
    page: int
    page_size: int
    total_items: int
    total_pages: int

@router.get("/", response_model=PaginatedResponse)
async def get_all_beef_cattle(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    breed: Optional[str] = Query(None, description="Filtrar por raça"),
    min_weight: Optional[float] = Query(None, description="Peso mínimo"),
    max_weight: Optional[float] = Query(None, description="Peso máximo")
):
    """
    Obtém todos os registros de bois para engorda, com opções de filtro e paginação.
    """
    try:
        filters = {
            "status": status,
            "breed": breed,
            "min_weight": min_weight,
            "max_weight": max_weight
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = beef_cattle_db.count_beef_cattle(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = beef_cattle_db.get_all_beef_cattle(filters, page, page_size)
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros: {str(e)}")

@router.post("/feeding", response_model=FeedingRecordResponse)
async def add_feeding_record(record: FeedingRecordCreate = Body(...)):
    """
    Adiciona um novo registro de alimentação.
    """
    try:
        result = beef_cattle_db.add_feeding_record(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar registro de alimentação: {str(e)}")

@router.get("/feeding/{cattle_id}", response_model=PaginatedResponse)
async def get_feeding_records(
    cattle_id: int = Path(..., description="ID do boi"),
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Obtém registros de alimentação para um boi específico com paginação.
    """
    try:
        # Converter strings para objetos date
        start_date_obj = None
        end_date_obj = None
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inicial inválido. Use o formato YYYY-MM-DD.")
                
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data final inválido. Use o formato YYYY-MM-DD.")
        
        filters = {
            "cattle_id": cattle_id,
            "start_date": start_date_obj,
            "end_date": end_date_obj
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = beef_cattle_db.count_feeding_records(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = beef_cattle_db.get_feeding_records(filters, page, page_size)
        
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
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de alimentação: {str(e)}")

# Health records endpoints
@router.post("/health", response_model=HealthRecordResponse)
async def add_health_record(record: HealthRecordCreate = Body(...)):
    """
    Adiciona um novo registro de saúde.
    """
    try:
        result = beef_cattle_db.add_health_record(record.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar registro de saúde: {str(e)}")

@router.get("/health/{cattle_id}", response_model=PaginatedResponse)
async def get_health_records(
    cattle_id: int = Path(..., description="ID do boi"),
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)"),
    record_type: Optional[str] = Query(None, description="Tipo de registro")
):
    """
    Obtém registros de saúde para um boi específico com paginação.
    """
    try:
        # Converter strings para objetos date
        start_date_obj = None
        end_date_obj = None
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inicial inválido. Use o formato YYYY-MM-DD.")
                
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data final inválido. Use o formato YYYY-MM-DD.")
        
        filters = {
            "cattle_id": cattle_id,
            "start_date": start_date_obj,
            "end_date": end_date_obj,
            "record_type": record_type
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = beef_cattle_db.count_health_records(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = beef_cattle_db.get_health_records(filters, page, page_size)
        
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
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de saúde: {str(e)}")

# Sale records endpoints
# Weight records endpoints
@router.post("/weights", response_model=WeightRecordResponse)
async def add_weight_record(record: WeightRecordCreate = Body(...)):
    """
    Adiciona um novo registro de pesagem.
    """
    try:
        result = beef_cattle_db.add_weight_record(record.dict())
        # Update current weight in beef_cattle table
        beef_cattle_db.update_beef_cattle(record.cattle_id, {"current_weight": record.weight})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar registro de peso: {str(e)}")

@router.get("/weights/{cattle_id}", response_model=PaginatedResponse)
async def get_weight_records(
    cattle_id: int = Path(..., description="ID do boi"),
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página"),
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Obtém registros de pesagem para um boi específico com paginação.
    """
    try:
        # Converter strings para objetos date
        start_date_obj = None
        end_date_obj = None
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inicial inválido. Use o formato YYYY-MM-DD.")
                
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data final inválido. Use o formato YYYY-MM-DD.")
        
        filters = {
            "cattle_id": cattle_id,
            "start_date": start_date_obj,
            "end_date": end_date_obj
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = beef_cattle_db.count_weight_records(filters)
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = beef_cattle_db.get_weight_records(filters, page, page_size)
        
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
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de peso: {str(e)}")

# Feeding records endpoints
@router.post("/sales", response_model=SaleRecordResponse)
async def add_sale_record(record: SaleRecordCreate = Body(...)):
    """
    Adiciona um novo registro de venda/abate.
    """
    try:
        result = beef_cattle_db.add_sale_record(record.dict())
        # Update status in beef_cattle table
        beef_cattle_db.update_beef_cattle(record.cattle_id, {"status": "Vendido"})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar registro de venda: {str(e)}")

class SalesFilterParams(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    page: int = 1
    page_size: int = 10

@router.post("/sales/search", response_model=PaginatedResponse)
async def search_sale_records(filters: SalesFilterParams = Body(...)):
    """
    Obtém registros de venda/abate com filtros enviados no body e paginação.
    """
    try:
        # Converter strings para objetos date
        start_date_obj = None
        end_date_obj = None
        
        if filters.start_date:
            try:
                start_date_obj = datetime.strptime(filters.start_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inicial inválido. Use o formato YYYY-MM-DD.")
                
        if filters.end_date:
            try:
                end_date_obj = datetime.strptime(filters.end_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data final inválido. Use o formato YYYY-MM-DD.")
        
        filter_dict = {
            "start_date": start_date_obj,
            "end_date": end_date_obj
        }
        # Remove None values
        filter_dict = {k: v for k, v in filter_dict.items() if v is not None}
        
        # Obter total de registros para calcular total de páginas
        total_items = beef_cattle_db.count_sale_records(filter_dict)
        total_pages = (total_items + filters.page_size - 1) // filters.page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = beef_cattle_db.get_sale_records(filter_dict, filters.page, filters.page_size)
        
        return {
            "items": items,
            "page": filters.page,
            "page_size": filters.page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de venda: {str(e)}")

@router.get("/sales", response_model=PaginatedResponse)
async def get_sale_records(
    page: int = Query(1, ge=1, description="Página atual"),
    page_size: int = Query(10, ge=1, le=100, description="Itens por página")
):
    """
    Obtém todos os registros de venda/abate sem filtros, com paginação.
    """
    try:
        # Obter total de registros para calcular total de páginas
        total_items = beef_cattle_db.count_sale_records({})
        total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1
        
        # Obter registros paginados
        items = beef_cattle_db.get_sale_records({}, page, page_size)
        
        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de venda: {str(e)}")

# Dashboard data endpoints
@router.get("/dashboard/summary")
async def get_dashboard_summary():
    """
    Obtém dados resumidos para o dashboard de boi gordo.
    """
    try:
        result = beef_cattle_db.get_dashboard_summary()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter resumo do dashboard: {str(e)}")

@router.get("/dashboard/weight-gain")
async def get_weight_gain_data(
    start_date: Optional[str] = Query(None, description="Data inicial (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Data final (YYYY-MM-DD)")
):
    """
    Obtém dados de ganho de peso para o dashboard.
    """
    try:
        # Converter strings para objetos date
        start_date_obj = None
        end_date_obj = None
        
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inicial inválido. Use o formato YYYY-MM-DD.")
                
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data final inválido. Use o formato YYYY-MM-DD.")
        
        filters = {
            "start_date": start_date_obj,
            "end_date": end_date_obj
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        result = beef_cattle_db.get_weight_gain_data(filters)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados de ganho de peso: {str(e)}")

# --- AGORA, DEIXE AS ROTAS DINÂMICAS POR ÚLTIMO ---
@router.get("/{cattle_id}", response_model=BeefCattleResponse)
async def get_beef_cattle(cattle_id: int = Path(..., description="ID do boi")):
    """
    Obtém um registro específico de boi para engorda pelo ID.
    """
    try:
        result = beef_cattle_db.get_beef_cattle_by_id(cattle_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Boi com ID {cattle_id} não encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registro: {str(e)}")

@router.put("/{cattle_id}", response_model=BeefCattleResponse)
async def update_beef_cattle(
    cattle_id: int = Path(..., description="ID do boi"),
    cattle_data: BeefCattleUpdate = Body(...)
):
    """
    Atualiza um registro de boi para engorda.
    """
    try:
        update_data = {k: v for k, v in cattle_data.dict().items() if v is not None}
        result = beef_cattle_db.update_beef_cattle(cattle_id, update_data)
        if not result:
            raise HTTPException(status_code=404, detail=f"Boi com ID {cattle_id} não encontrado")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar registro: {str(e)}")

@router.delete("/{cattle_id}")
async def delete_beef_cattle(cattle_id: int = Path(..., description="ID do boi")):
    """
    Remove um registro de boi para engorda.
    """
    try:
        success = beef_cattle_db.delete_beef_cattle(cattle_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Boi com ID {cattle_id} não encontrado")
        return {"message": f"Boi com ID {cattle_id} removido com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover registro: {str(e)}")
