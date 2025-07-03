from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from datetime import date
from pydantic import BaseModel
from backend.milk_database_query import milk_db_query

router = APIRouter(
    prefix="/api/milk",
    tags=["Milk Production"],
    responses={404: {"description": "Not found"}},
)

class DailyProductionFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    user_id: Optional[int] = None
    animal_id: Optional[int] = None

@router.post("/daily-production")
async def get_daily_production(
    filter_params: DailyProductionFilter = Body(..., example={"start_date": "2023-01-01", "end_date": "2023-12-31"})
) -> List[Dict[str, Any]]:
    """
    Obtém dados de produção diária de leite filtrados por período, usuário e animal.
    
    Parâmetros no body:
    - **start_date**: Data de início para filtrar registros de produção
    - **end_date**: Data de fim para filtrar registros de produção
    - **user_id**: ID do usuário para filtrar registros de produção
    - **animal_id**: ID do animal para filtrar registros de produção
    
    Retorna uma lista de registros diários com o total de litros produzidos.
    """
    try:
        results = milk_db_query.get_daily_milk_production(
            start_date=filter_params.start_date,
            end_date=filter_params.end_date,
            user_id=filter_params.user_id,
            animal_id=filter_params.animal_id
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter produção diária: {str(e)}")