from fastapi import APIRouter, HTTPException, Body, Query
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.milk_database_query import milk_db_query

router = APIRouter(
    prefix="/api/milk",
    tags=["Milk Price"],
    responses={404: {"description": "Not found"}},
)

class MilkPriceUpdate(BaseModel):
    net_price_avg: float = Field(..., description="Preço médio líquido", ge=0)
    dairy_percentage: float = Field(..., description="Percentual do laticínio", ge=0, le=1)

@router.get("/price/current")
async def get_current_milk_price() -> Dict[str, Any]:
    """
    Obtém o preço atual do leite e informações relacionadas.
    
    Retorna um dicionário com o preço atual do leite e informações relacionadas.
    """
    try:
        result = milk_db_query.get_current_milk_price()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter preço atual do leite: {str(e)}")

@router.get("/price/history")
async def get_milk_price_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(6, ge=1, le=12)
) -> Dict[str, Any]:
    """
    Obtém o histórico de preços do leite com paginação.
    
    - **page**: Número da página
    - **page_size**: Tamanho da página
    
    Retorna uma lista de registros de preços e informações de paginação.
    """
    try:
        result = milk_db_query.get_milk_price_history(page, page_size)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter histórico de preços do leite: {str(e)}")

@router.post("/price/update")
async def update_milk_price(
    price_update: MilkPriceUpdate = Body(..., example={"net_price_avg": 2.75, "dairy_percentage": 0.15})
) -> Dict[str, Any]:
    """
    Atualiza o preço do leite para o mês atual.
    
    - **net_price_avg**: Preço médio líquido
    - **dairy_percentage**: Percentual do laticínio
    
    Retorna o novo preço do leite e informações relacionadas.
    """
    try:
        result = milk_db_query.update_milk_price(
            net_price_avg=price_update.net_price_avg,
            dairy_percentage=price_update.dairy_percentage
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar preço do leite: {str(e)}")