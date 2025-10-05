#!/usr/bin/env python3
"""
Script para testar o endpoint de criação de plantas.
"""

import requests
import json

def test_plant_creation():
    """Testa a criação de uma planta via API."""
    url = "http://localhost:8000/api/floriculture/plant"
    
    plant_data = {
        "user_id": 1,
        "name": "Rosa Teste API",
        "scientific_name": "Rosa api",
        "category": "Flores",
        "environment": "Externo",
        "sun_needs": "Pleno Sol",
        "watering": "Diária",
        "stock": 15,
        "price": 25.50,
        "description": "Planta criada via API",
        "care_instructions": "Cuidados via API"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testando criação de planta via API...")
        print(f"URL: {url}")
        print(f"Dados: {json.dumps(plant_data, indent=2)}")
        
        response = requests.post(url, json=plant_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"OK - Planta criada com sucesso: ID {result['id']}")
            return True
        else:
            print(f"ERRO - Falha na criação: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERRO - Exceção: {e}")
        return False

def test_plant_listing():
    """Testa a listagem de plantas via API."""
    url = "http://localhost:8000/api/floriculture/plant"
    
    try:
        print("\nTestando listagem de plantas via API...")
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"OK - {len(result['items'])} plantas encontradas")
            return True
        else:
            print(f"ERRO - Falha na listagem: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERRO - Exceção: {e}")
        return False

def main():
    """Função principal."""
    print("Testando endpoints de plantas...")
    print("=" * 50)
    
    # Teste 1: Criação
    success1 = test_plant_creation()
    
    # Teste 2: Listagem
    success2 = test_plant_listing()
    
    print("=" * 50)
    if success1 and success2:
        print("Todos os testes passaram!")
    else:
        print("Alguns testes falharam.")

if __name__ == "__main__":
    main()