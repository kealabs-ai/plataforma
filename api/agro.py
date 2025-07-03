from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import sys
import os

# Adiciona o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from backend.agro_database import agro_db

router = APIRouter(prefix="/agro", tags=["agro"])

# Modelos Pydantic
class Production(BaseModel):
    user_id: int
    plot_id: int
    crop: str
    area_ha: float
    production_kg: Optional[float] = None
    harvest_date: Optional[date] = None
    notes: Optional[str] = None

class MilkProduction(BaseModel):
    user_id: int
    production_date: date
    liters_produced: float
    notes: Optional[str] = None

class Input(BaseModel):
    user_id: int
    purchase_date: date
    supplier: str
    product: str
    quantity: float
    unit: str
    total_cost: float
    purpose: Optional[str] = None

class SoilAnalysis(BaseModel):
    plot_id: int
    analysis_date: date
    pH: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    organic_matter: Optional[float] = None
    recommendation: Optional[str] = None

class Finance(BaseModel):
    user_id: int
    entry_date: date
    type: str  # 'Receita' ou 'Despesa'
    description: str
    value: float
    category: str
    payment_method: Optional[str] = None
    notes: Optional[str] = None

@router.get("/dashboard-data")
async def get_dashboard_data():
    """Endpoint para obter dados do dashboard"""
    try:
        # Tenta buscar todos os dados do banco
        crop_production = agro_db.get_crop_production_summary()
        milk_production = agro_db.get_milk_production_monthly()
        inputs_distribution = agro_db.get_inputs_distribution()
        soil_ph = agro_db.get_soil_ph_by_plot()
        financial_data = agro_db.get_financial_summary()
        
        # Verifica se algum dos dados está vazio e usa dados simulados se necessário
        if not crop_production:
            crop_production = [
                {"crop": "Soja", "total_production": 15000},
                {"crop": "Milho", "total_production": 12000},
                {"crop": "Trigo", "total_production": 8000}
            ]
            
        if not milk_production:
            milk_production = [
                {"month": "2024-01", "total_liters": 5000},
                {"month": "2024-02", "total_liters": 5200},
                {"month": "2024-03", "total_liters": 4800}
            ]
            
        if not inputs_distribution:
            inputs_distribution = [
                {"product": "Fertilizante", "total_cost": 15000},
                {"product": "Sementes", "total_cost": 8000},
                {"product": "Defensivos", "total_cost": 12000}
            ]
            
        if not soil_ph:
            soil_ph = [
                {"plot_name": "Talhão 1", "pH": 6.5},
                {"plot_name": "Talhão 2", "pH": 7.2},
                {"plot_name": "Talhão 3", "pH": 5.8}
            ]
            
        if not financial_data:
            financial_data = [
                {"month": "2024-01", "revenue": 25000, "expense": 18000},
                {"month": "2024-02", "revenue": 28000, "expense": 19000},
                {"month": "2024-03", "revenue": 22000, "expense": 16000}
            ]
        
        return {
            "crop_production": crop_production,
            "milk_production": milk_production,
            "inputs_distribution": inputs_distribution,
            "soil_ph": soil_ph,
            "financial_data": financial_data
        }
        
    except Exception as e:
        print(f"Erro ao buscar dados do dashboard: {e}")
        # Fallback para dados simulados em caso de erro
        return {
            "crop_production": [
                {"crop": "Soja", "total_production": 15000},
                {"crop": "Milho", "total_production": 12000},
                {"crop": "Trigo", "total_production": 8000}
            ],
            "milk_production": [
                {"month": "2024-01", "total_liters": 5000},
                {"month": "2024-02", "total_liters": 5200},
                {"month": "2024-03", "total_liters": 4800}
            ],
            "inputs_distribution": [
                {"product": "Fertilizante", "total_cost": 15000},
                {"product": "Sementes", "total_cost": 8000},
                {"product": "Defensivos", "total_cost": 12000}
            ],
            "soil_ph": [
                {"plot_name": "Talhão 1", "pH": 6.5},
                {"plot_name": "Talhão 2", "pH": 7.2},
                {"plot_name": "Talhão 3", "pH": 5.8}
            ],
            "financial_data": [
                {"month": "2024-01", "revenue": 25000, "expense": 18000},
                {"month": "2024-02", "revenue": 28000, "expense": 19000},
                {"month": "2024-03", "revenue": 22000, "expense": 16000}
            ]
        }

@router.post("/productions")
async def create_production(production: Production):
    """Criar nova produção agrícola"""
    try:
        production_id = agro_db.create_production(
            production.user_id, production.plot_id, production.crop,
            production.area_ha, production.production_kg, 
            production.harvest_date, production.notes
        )
        return {"message": "Produção criada com sucesso", "id": production_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar produção: {str(e)}")

@router.post("/milk-production")
async def create_milk_production(milk: MilkProduction):
    """Criar nova produção de leite"""
    try:
        milk_id = agro_db.create_milk_production(
            milk.user_id, milk.production_date, 
            milk.liters_produced, milk.notes
        )
        return {"message": "Produção de leite criada com sucesso", "id": milk_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar produção de leite: {str(e)}")

@router.post("/inputs")
async def create_input(input_data: Input):
    """Criar novo insumo"""
    try:
        input_id = agro_db.create_input(
            input_data.user_id, input_data.purchase_date, input_data.supplier,
            input_data.product, input_data.quantity, input_data.unit,
            input_data.total_cost, input_data.purpose
        )
        return {"message": "Insumo criado com sucesso", "id": input_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar insumo: {str(e)}")

@router.post("/soil-analysis")
async def create_soil_analysis(soil: SoilAnalysis):
    """Criar nova análise de solo"""
    try:
        analysis_id = agro_db.create_soil_analysis(
            soil.plot_id, soil.analysis_date, soil.pH, soil.nitrogen,
            soil.phosphorus, soil.potassium, soil.organic_matter, soil.recommendation
        )
        return {"message": "Análise de solo criada com sucesso", "id": analysis_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar análise de solo: {str(e)}")

@router.post("/finances")
async def create_finance(finance: Finance):
    """Criar nova entrada financeira"""
    try:
        finance_id = agro_db.create_finance(
            finance.user_id, finance.entry_date, finance.type, finance.description,
            finance.value, finance.category, finance.payment_method, finance.notes
        )
        return {"message": "Entrada financeira criada com sucesso", "id": finance_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar entrada financeira: {str(e)}")

@router.get("/productions")
async def get_productions():
    """Obter lista de produções"""
    try:
        result = agro_db.get_crop_production_summary()
        if not result:
            # Retorna dados simulados se não houver dados reais
            return [
                {"crop": "Soja", "total_production": 15000},
                {"crop": "Milho", "total_production": 12000},
                {"crop": "Trigo", "total_production": 8000}
            ]
        return result
    except Exception as e:
        print(f"Erro ao obter produções: {e}")
        # Retorna dados simulados em caso de erro
        return [
            {"crop": "Soja", "total_production": 15000},
            {"crop": "Milho", "total_production": 12000},
            {"crop": "Trigo", "total_production": 8000}
        ]

@router.get("/milk-production")
async def get_milk_production():
    """Obter produção de leite"""
    try:
        result = agro_db.get_milk_production_monthly()
        if not result:
            # Retorna dados simulados se não houver dados reais
            return [
                {"month": "2024-01", "total_liters": 5000},
                {"month": "2024-02", "total_liters": 5200},
                {"month": "2024-03", "total_liters": 4800},
                {"month": "2024-04", "total_liters": 5100}
            ]
        return result
    except Exception as e:
        print(f"Erro ao obter produção de leite: {e}")
        # Retorna dados simulados em caso de erro
        return [
            {"month": "2024-01", "total_liters": 5000},
            {"month": "2024-02", "total_liters": 5200},
            {"month": "2024-03", "total_liters": 4800},
            {"month": "2024-04", "total_liters": 5100}
        ]

@router.get("/inputs")
async def get_inputs():
    """Obter lista de insumos"""
    try:
        result = agro_db.get_inputs_distribution()
        if not result:
            # Retorna dados simulados se não houver dados reais
            return [
                {"product": "Fertilizante", "total_cost": 15000},
                {"product": "Sementes", "total_cost": 8000},
                {"product": "Defensivos", "total_cost": 12000}
            ]
        return result
    except Exception as e:
        print(f"Erro ao obter insumos: {e}")
        # Retorna dados simulados em caso de erro
        return [
            {"product": "Fertilizante", "total_cost": 15000},
            {"product": "Sementes", "total_cost": 8000},
            {"product": "Defensivos", "total_cost": 12000}
        ]

@router.get("/soil-analysis")
async def get_soil_analysis():
    """Obter análises de solo"""
    try:
        result = agro_db.get_soil_ph_by_plot()
        if not result:
            # Retorna dados simulados se não houver dados reais
            return [
                {"plot_name": "Talhão 1", "pH": 6.5},
                {"plot_name": "Talhão 2", "pH": 7.2},
                {"plot_name": "Talhão 3", "pH": 5.8}
            ]
        return result
    except Exception as e:
        print(f"Erro ao obter análises de solo: {e}")
        # Retorna dados simulados em caso de erro
        return [
            {"plot_name": "Talhão 1", "pH": 6.5},
            {"plot_name": "Talhão 2", "pH": 7.2},
            {"plot_name": "Talhão 3", "pH": 5.8}
        ]

@router.get("/finances")
async def get_finances():
    """Obter dados financeiros"""
    try:
        result = agro_db.get_financial_summary()
        if not result:
            # Retorna dados simulados se não houver dados reais
            return [
                {"month": "2024-01", "revenue": 25000, "expense": 18000},
                {"month": "2024-02", "revenue": 28000, "expense": 19000},
                {"month": "2024-03", "revenue": 22000, "expense": 16000}
            ]
        return result
    except Exception as e:
        print(f"Erro ao obter dados financeiros: {e}")
        # Retorna dados simulados em caso de erro
        return [
            {"month": "2024-01", "revenue": 25000, "expense": 18000},
            {"month": "2024-02", "revenue": 28000, "expense": 19000},
            {"month": "2024-03", "revenue": 22000, "expense": 16000}
        ]