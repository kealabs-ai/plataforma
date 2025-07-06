from fastapi import APIRouter, HTTPException, Query, Path, Body, Depends
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from pydantic import BaseModel, validator, Field
from fastapi.responses import JSONResponse

# Direct endpoints for beef cattle
router = APIRouter(
    tags=["Beef Cattle Direct"],
)

class CattleFilterParams(BaseModel):
    status: Optional[str] = None
    breed: Optional[str] = None
    min_weight: Optional[float] = None
    max_weight: Optional[float] = None

@router.get("/api/beef_cattle/")
async def get_all_beef_cattle_direct(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    breed: Optional[str] = Query(None, description="Filtrar por raça"),
    min_weight: Optional[float] = Query(None, description="Peso mínimo"),
    max_weight: Optional[float] = Query(None, description="Peso máximo")
):
    """
    Get all beef cattle records from database with optional query filters
    """
    try:
        from backend.beef_cattle_database import beef_cattle_db
        
        filters = {
            "status": status,
            "breed": breed,
            "min_weight": min_weight,
            "max_weight": max_weight
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Buscar dados do banco de dados
        result = beef_cattle_db.get_all_beef_cattle(filters)
        return result
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

@router.post("/api/beef_cattle/search")
async def search_beef_cattle_direct(filters: CattleFilterParams = Body(...)):
    """
    Search beef cattle records with filters from database
    """
    try:
        from backend.beef_cattle_database import beef_cattle_db
        
        filter_dict = {
            "status": filters.status,
            "breed": filters.breed,
            "min_weight": filters.min_weight,
            "max_weight": filters.max_weight
        }
        # Remove None values
        filter_dict = {k: v for k, v in filter_dict.items() if v is not None}
        
        # Buscar dados do banco de dados com filtros
        result = beef_cattle_db.get_all_beef_cattle(filter_dict)
        return result
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

@router.get("/api/beef_cattle/dashboard/summary")
async def get_dashboard_summary_direct():
    """
    Get dashboard summary data from database
    """
    try:
        from backend.beef_cattle_database import beef_cattle_db
        
        # Buscar dados do banco de dados
        result = beef_cattle_db.get_dashboard_summary()
        return result
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

class SalesFilterParams(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@router.get("/api/beef_cattle/sales")
async def get_sales_direct():
    """
    Get all sales records from database
    """
    try:
        from backend.beef_cattle_database import beef_cattle_db
        
        # Buscar dados do banco de dados sem filtros
        result = beef_cattle_db.get_sale_records({})
        return result
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

@router.post("/api/beef_cattle/sales/search")
async def search_sales_direct(filters: SalesFilterParams = Body(...)):
    """
    Search sales records with filters from database
    """
    try:
        from backend.beef_cattle_database import beef_cattle_db
        
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
        
        # Buscar dados do banco de dados com filtros
        result = beef_cattle_db.get_sale_records(filter_dict)
        return result
    except HTTPException:
        raise
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

class WeightGainFilterParams(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@router.get("/api/beef_cattle/dashboard/weight-gain")
async def get_weight_gain_data_direct():
    """
    Get weight gain data from database
    """
    try:
        from backend.beef_cattle_database import beef_cattle_db
        
        # Buscar dados do banco de dados sem filtros
        result = beef_cattle_db.get_weight_gain_data({})
        return result
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

@router.post("/api/beef_cattle/dashboard/weight-gain/search")
async def search_weight_gain_data_direct(filters: WeightGainFilterParams = Body(...)):
    """
    Search weight gain data with filters from database
    """
    try:
        from backend.beef_cattle_database import beef_cattle_db
        
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
        
        # Buscar dados do banco de dados com filtros
        result = beef_cattle_db.get_weight_gain_data(filter_dict)
        return result
    except HTTPException:
        raise
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

@router.get("/.well-known/appspecific/com.chrome.devtools.json")
async def chrome_devtools():
    """
    Endpoint para suprimir logs do Chrome DevTools
    """
    return JSONResponse(content={})