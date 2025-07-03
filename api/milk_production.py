from fastapi import APIRouter, HTTPException, Query, Path, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import sys
import os

# Adiciona o diretório raiz ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from backend.milk_database import milk_db

router = APIRouter(prefix="/api/milk", tags=["milk_production"])

# --- Modelos Pydantic ---
# Os modelos Pydantic definem a estrutura dos dados para validação e serialização.
class AnimalCreate(BaseModel):
    official_id: str
    name: Optional[str] = None
    birth_date: date
    breed: Optional[str] = None
    gender: str
    status: Optional[str] = None
    entry_date: Optional[date] = None # Corrigido para date, para ser consistente com o modelo de banco de dados

class AnimalResponse(BaseModel):
    animal_id: int
    official_id: str
    name: Optional[str] = None
    birth_date: date
    breed: Optional[str] = None
    gender: str
    status: Optional[str] = None
    entry_date: Optional[date] = None

class MilkProductionEntry(BaseModel):
    animal_id: int
    production_date: date
    quantity: float
    period: str  # 'morning', 'afternoon', 'night'
    notes: Optional[str] = None

class MilkProductionResponse(BaseModel):
    # Campos do registro de produção
    id: int
    animal_id: int
    production_date: date
    liters_produced: float
    period: str
    notes: Optional[str] = None
    quantity: float # Mapeamento duplicado para compatibilidade
    
    # Campos do animal relacionado
    name: Optional[str] = None
    official_id: Optional[str] = None
    breed: Optional[str] = None
    status: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    entry_date: Optional[date] = None
    age: Optional[int] = None # Adicionado o campo age, calculado no backend

class MilkProductionUpdate(BaseModel):
    quantity: Optional[float] = None
    period: Optional[str] = None
    notes: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int

# Modelo para a resposta da produção mensal por usuário
class MonthlyMilkProductionResponse(BaseModel):
    month: str
    total_liters: float

# --- Endpoints para Animais ---
@router.post("/animals", response_model=AnimalResponse)
async def create_animal(animal: AnimalCreate):
    """Cria um novo animal"""
    try:
        animal_id = milk_db.create_animal(
            official_id=animal.official_id,
            name=animal.name,
            birth_date=animal.birth_date,
            breed=animal.breed,
            gender=animal.gender,
            status=animal.status,
            entry_date=animal.entry_date
        )
        if animal_id is None:
            raise HTTPException(status_code=500, detail="Falha ao criar animal no banco de dados.")
            
        # Retorna o objeto completo com o ID gerado
        return AnimalResponse(animal_id=animal_id, **animal.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar animal: {str(e)}")

@router.get("/animals", response_model=List[AnimalResponse])
async def get_animals():
    """Obtém a lista de todos os animais ativos"""
    try:
        animals = milk_db.get_animals()
        # Se não houver dados, retorna uma lista vazia, evitando a simulação aqui
        return animals if animals else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter animais: {str(e)}")

@router.get("/animals/{animal_id}", response_model=AnimalResponse)
async def get_animal(animal_id: int = Path(..., title="ID do animal")):
    """Obtém um animal pelo ID"""
    try:
        animal = milk_db.get_animal(animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        return animal
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter animal: {str(e)}")

@router.put("/animals/{animal_id}", response_model=AnimalResponse)
async def update_animal(animal: AnimalCreate, animal_id: int = Path(..., title="ID do animal")):
    """Atualiza um animal existente"""
    try:
        updated = milk_db.update_animal(
            animal_id=animal_id,
            official_id=animal.official_id,
            name=animal.name,
            birth_date=animal.birth_date,
            breed=animal.breed,
            gender=animal.gender,
            status=animal.status,
            entry_date=animal.entry_date
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        # Busca o animal atualizado para garantir que a resposta esteja completa e consistente
        updated_animal_data = milk_db.get_animal(animal_id)
        if not updated_animal_data:
            # Caso o animal seja encontrado e depois não, é um erro de lógica
            raise HTTPException(status_code=500, detail="Animal atualizado, mas não pôde ser recuperado.")
            
        return updated_animal_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar animal: {str(e)}")

@router.delete("/animals/{animal_id}")
async def delete_animal(animal_id: int = Path(..., title="ID do animal")):
    """Inativa um animal (altera o status para 'Inativo')"""
    try:
        deleted = milk_db.delete_animal(animal_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        return {"message": f"Animal com ID {animal_id} inativado com sucesso."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inativar animal: {str(e)}")

# --- Endpoints para Produção de Leite ---
@router.post("/production", response_model=MilkProductionResponse)
async def create_milk_production(production: MilkProductionEntry):
    """Cria um novo registro de produção de leite"""
    try:
        # Verificar se o animal existe
        animal = milk_db.get_animal(production.animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail="Animal não encontrado")
        
        production_id = milk_db.create_milk_production_entry(
            animal_id=production.animal_id,
            production_date=production.production_date,
            liters_produced=production.quantity, # Mapeamento de 'quantity' para 'liters_produced'
            period=production.period,
            notes=production.notes
        )
        
        if production_id is None:
            raise HTTPException(status_code=500, detail="Falha ao criar registro de produção.")
            
        # Obter o registro completo com dados do animal para a resposta
        created_entry = milk_db.get_milk_production_entry(production_id)
        
        return created_entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar registro de produção: {str(e)}")

@router.get("/production", response_model=PaginatedResponse)
async def get_milk_production(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100), # Ajustado o tamanho da página para um valor mais comum
    animal_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Obtém registros de produção de leite com paginação e filtros"""
    try:
        # Obter total de registros para paginação
        total = milk_db.count_milk_production_entries(animal_id, start_date, end_date)
        
        # Calcular total de páginas
        total_pages = (total + page_size - 1) // page_size
        
        # Obter registros da página atual
        entries = milk_db.get_milk_production_entries(
            page=page, 
            page_size=page_size, 
            animal_id=animal_id, 
            start_date=start_date, 
            end_date=end_date
        )
        
        # Removido a lógica de dados simulados do código de produção
        
        return {
            "items": entries,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registros de produção: {str(e)}")

@router.get("/production/{production_id}", response_model=MilkProductionResponse)
async def get_milk_production_entry(production_id: int = Path(..., title="ID do registro de produção")):
    """Obtém um registro de produção de leite por ID"""
    try:
        entry = milk_db.get_milk_production_entry(production_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Registro de produção não encontrado")
        return entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter registro de produção: {str(e)}")

@router.put("/production/{production_id}", response_model=MilkProductionResponse)
async def update_milk_production(
    production: MilkProductionUpdate,
    production_id: int = Path(..., title="ID do registro de produção")
):
    """Atualiza um registro de produção de leite"""
    try:
        # Verificar se o registro existe
        entry = milk_db.get_milk_production_entry(production_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Registro de produção não encontrado")
        
        updated = milk_db.update_milk_production_entry(
            entry_id=production_id,
            liters_produced=production.quantity, # Mapeamento de 'quantity' para 'liters_produced'
            period=production.period,
            notes=production.notes
        )
        
        if not updated:
            raise HTTPException(status_code=500, detail="Falha ao atualizar registro de produção")
        
        # Obter o registro atualizado para retornar na resposta
        updated_entry = milk_db.get_milk_production_entry(production_id)
        if not updated_entry:
            # Erro de lógica se o registro foi atualizado mas não pode ser recuperado
            raise HTTPException(status_code=500, detail="Registro atualizado, mas não pôde ser recuperado.")
            
        return updated_entry
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar registro de produção: {str(e)}")

@router.delete("/production/{production_id}")
async def delete_milk_production(production_id: int = Path(..., title="ID do registro de produção")):
    """Exclui um registro de produção de leite"""
    try:
        deleted = milk_db.delete_milk_production_entry(production_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Registro de produção não encontrado")
        return {"message": f"Registro de produção com ID {production_id} excluído com sucesso."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir registro de produção: {str(e)}")

# --- Endpoints para Dashboard de Produção de Leite ---
@router.get("/dashboard")
async def get_milk_dashboard(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    """Obtém dados para o dashboard de produção de leite"""
    try:
        # Produção diária
        daily_production = milk_db.get_daily_milk_production(start_date, end_date)
        
        # Produção por animal
        animal_production = milk_db.get_milk_production_by_animal()
        
        return {
            "daily_production": daily_production,
            "animal_production": animal_production
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter dados do dashboard: {str(e)}")
   
class AnimalCountResponse(BaseModel):
    total_animals: int

@router.get("/animals/total_count", response_model=AnimalCountResponse)
async def get_animal_count():
    try:
        count = milk_db.count_animals()
        print("DEBUG count:", count, type(count))  # <-- Adicione esta linha
        total = count if count is not None else 0
        return AnimalCountResponse(total_animals=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter a contagem de animais: {str(e)}")

### **Novos Endpoints Adicionados:**

#### **1. Produção Mensal de Leite por Usuário**
@router.get("/production/monthly_by_user/{user_id}", response_model=List[MonthlyMilkProductionResponse], tags=["Milk Production"])
async def get_monthly_milk_production_by_user_endpoint(
    user_id: int = Path(..., title="ID do usuário"),
    start_date: date = Query(..., description="Data de início (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Data de fim (YYYY-MM-DD)")
):
    """
    **Obtém a quantidade total de litros de leite produzida por mês por um usuário específico dentro de um período definido.**

    - `user_id`: O ID do usuário para filtrar a produção de leite.
    - `start_date`: A data de início (YYYY-MM-DD) para a consulta.
    - `end_date`: A data de fim (YYYY-MM-DD) para a consulta.
    """
    try:
        monthly_production = milk_db.get_monthly_milk_production_by_user(user_id, start_date, end_date)
        if not monthly_production:
            raise HTTPException(status_code=404, detail="Nenhum registro de produção mensal encontrado para o usuário no período especificado.")
        return monthly_production
    except Exception as e :
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor ao obter produção mensal por usuário: {str(e)}")