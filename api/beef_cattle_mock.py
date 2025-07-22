from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import date
from database_queries.beef_cattle_database_simple import beef_cattle_db_simple

router = APIRouter(
    prefix="/api/beef_cattle_mock",
    tags=["Beef Cattle Mock"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_all_beef_cattle_mock(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    breed: Optional[str] = Query(None, description="Filtrar por raça"),
    min_weight: Optional[float] = Query(None, description="Peso mínimo"),
    max_weight: Optional[float] = Query(None, description="Peso máximo")
):
    """
    Get all beef cattle records with optional filters
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
        
        result = beef_cattle_db_simple.get_all_beef_cattle(filters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting beef cattle: {str(e)}")

@router.get("/dashboard/summary")
async def get_dashboard_summary_mock():
    """
    Get dashboard summary data
    """
    try:
        result = beef_cattle_db_simple.get_dashboard_summary()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dashboard summary: {str(e)}")

@router.get("/sales")
async def get_sales_mock(
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final")
):
    """
    Get sales records
    """
    try:
        filters = {
            "start_date": start_date,
            "end_date": end_date
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        result = beef_cattle_db_simple.get_sale_records(filters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sales: {str(e)}")

@router.get("/dashboard/weight-gain")
async def get_weight_gain_data_mock(
    start_date: Optional[date] = Query(None, description="Data inicial"),
    end_date: Optional[date] = Query(None, description="Data final")
):
    """
    Get weight gain data
    """
    try:
        filters = {
            "start_date": start_date,
            "end_date": end_date
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        result = beef_cattle_db_simple.get_weight_gain_data(filters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting weight gain data: {str(e)}")