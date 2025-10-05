#!/usr/bin/env python3
"""
Teste usando o mesmo formato que o JavaScript está enviando.
"""

import requests
import json

def test_js_format():
    """Testa usando o formato exato do JavaScript."""
    url = "http://localhost:8000/api/floriculture/plant"
    
    # Dados no formato que o JavaScript envia
    plant_data = {
        "name": "Rosa JavaScript",
        "scientific_name": "Rosa js",
        "category": "Flores",
        "environment": "Externo", 
        "sun_needs": "Pleno Sol",
        "watering": "Diária",
        "stock": "20",  # JavaScript pode enviar como string
        "price": "30.00",  # JavaScript pode enviar como string
        "image_url": "",
        "description": "Planta criada via JavaScript",
        "care_instructions": "Cuidados JavaScript"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("Testando formato JavaScript...")
        print(f"Dados: {json.dumps(plant_data, indent=2)}")
        
        response = requests.post(url, json=plant_data, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"OK - Planta criada: ID {result['id']}")
            return True
        else:
            print(f"ERRO - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERRO - Exceção: {e}")
        return False

if __name__ == "__main__":
    test_js_format()