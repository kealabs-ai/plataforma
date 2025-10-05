#!/usr/bin/env python3
"""
Teste simples para identificar o problema na criação de plantas.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from floriculture import PlantCreate
from database_queries.floriculture_database_query import create_plant

def test_pydantic_model():
    """Testa se o modelo Pydantic está funcionando."""
    try:
        plant_data = {
            "user_id": 1,
            "name": "Rosa Teste",
            "scientific_name": "Rosa test",
            "category": "Flores",
            "environment": "Externo",
            "sun_needs": "Pleno Sol",
            "watering": "Diária",
            "stock": 10,
            "price": 15.50,
            "description": "Teste",
            "care_instructions": "Cuidados"
        }
        
        plant = PlantCreate(**plant_data)
        print(f"OK - Modelo Pydantic criado: {plant.dict()}")
        return plant
    except Exception as e:
        print(f"ERRO - Problema no modelo Pydantic: {e}")
        return None

def test_direct_db_call():
    """Testa chamada direta ao banco."""
    try:
        result = create_plant(
            user_id=1,
            name="Rosa Teste Direto",
            scientific_name="Rosa direct",
            category="Flores",
            environment="Externo",
            sun_needs="Pleno Sol",
            watering="Diária",
            stock=10,
            price=15.50,
            description="Teste direto",
            care_instructions="Cuidados diretos"
        )
        
        if result:
            print(f"OK - Planta criada diretamente: ID {result['id']}")
            return True
        else:
            print("ERRO - Falha na criação direta")
            return False
    except Exception as e:
        print(f"ERRO - Exceção na criação direta: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Teste simples de criação de plantas")
    print("=" * 40)
    
    # Teste 1: Modelo Pydantic
    plant = test_pydantic_model()
    if not plant:
        return
    
    # Teste 2: Chamada direta ao banco
    test_direct_db_call()

if __name__ == "__main__":
    main()