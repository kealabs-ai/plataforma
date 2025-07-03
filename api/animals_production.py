from fastapi import APIRouter, HTTPException, Query, Path, Body
from typing import List, Dict, Any, Optional
from datetime import date, datetime
from pydantic import BaseModel, validator
from backend.milk_database_query import milk_db_query

router = APIRouter(
    prefix="/api/milk",
    tags=["Milk Production"],
    responses={404: {"description": "Not found"}},
)

class AnimalProductionFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    user_id: Optional[int] = None
    
    @validator('start_date', 'end_date', pre=True)
    def validate_date(cls, value):
        if not value:
            return None
            
        if isinstance(value, date):
            return value
            
        try:
            # Tenta converter string para data
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError as e:
            # Captura o erro específico e fornece uma mensagem mais amigável
            error_msg = str(e)
            if "day is out of range for month" in error_msg or "day value is outside expected range" in error_msg:
                raise ValueError(f"Data inválida: o dia está fora do intervalo válido para o mês especificado. Verifique se o mês tem o número de dias correto.")
            elif "month must be in 1..12" in error_msg:
                raise ValueError(f"Data inválida: o mês deve estar entre 1 e 12.")
            else:
                raise ValueError(f"Formato de data inválido. Use o formato YYYY-MM-DD.")
        except Exception:
            raise ValueError(f"Formato de data inválido. Use o formato YYYY-MM-DD.")
            
        return value

@router.post("/animals-production")
async def get_animals_with_production(
    filter_params: AnimalProductionFilter = Body(..., example={"start_date": "2023-01-01", "end_date": "2023-12-31", "user_id": 1})
) -> List[Dict[str, Any]]:
    """
    Obtém dados de animais relacionados com produção de leite, filtrados por período e usuário.
    
    Parâmetros no body:
    - **start_date**: Data de início para filtrar registros de produção
    - **end_date**: Data de fim para filtrar registros de produção
    - **user_id**: ID do usuário para filtrar registros de produção
    
    Retorna uma lista de registros com dados de animais e suas produções de leite.
    """
    try:
        results = milk_db_query.get_animals_with_production(
            start_date=filter_params.start_date,
            end_date=filter_params.end_date,
            user_id=filter_params.user_id
        )
        return results
    except ValueError as e:
        # Erros de validação são retornados como 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Outros erros são retornados como 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"Erro ao obter animais com produção: {str(e)}")
