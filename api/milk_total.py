from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, Optional
from datetime import date
from pydantic import BaseModel
from backend.milk_database_query import milk_db_query

router = APIRouter(
    prefix="/api/milk",
    tags=["Milk Production"],
    responses={404: {"description": "Not found"}},
)

class TotalProductionFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    user_id: Optional[int] = None
    animal_id: Optional[int] = None

@router.post("/total-production")
async def get_total_milk_production(
    filter_params: TotalProductionFilter = Body(..., example={"start_date": "2025-01-01", "end_date": "2025-01-31", "user_id": 1})
) -> Dict[str, Any]:
    """
    Obtém o total de litros de leite produzidos em um período por um usuário.
    
    Parâmetros no body:
    - **start_date**: Data de início para filtrar registros de produção
    - **end_date**: Data de fim para filtrar registros de produção
    - **user_id**: ID do usuário para filtrar registros de produção
    
    Retorna o total de litros produzidos no período.
    """
    try:
        result = milk_db_query.get_total_milk_production(
            start_date=filter_params.start_date,
            end_date=filter_params.end_date,
            user_id=filter_params.user_id,
            animal_id=filter_params.animal_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter total de produção de leite: {str(e)}")