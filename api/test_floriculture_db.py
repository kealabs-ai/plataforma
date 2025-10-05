#!/usr/bin/env python3
"""
Script de teste para verificar a conexão com o banco de dados
e criar a tabela floriculture_plants se necessário.
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.connection import get_db_connection
from database_queries.floriculture_database_query import create_plant

def test_database_connection():
    """Testa a conexão com o banco de dados."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print("OK - Conexão com banco de dados OK")
        return True
    except Exception as e:
        print(f"ERRO - Erro na conexão com banco de dados: {e}")
        return False

def create_floriculture_plants_table():
    """Cria a tabela floriculture_plants se não existir."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se a tabela existe
        cursor.execute("SHOW TABLES LIKE 'floriculture_plants'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Tabela floriculture_plants não existe. Criando...")
            
            cursor.execute("""
                CREATE TABLE floriculture_plants (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL DEFAULT 1,
                    name VARCHAR(100) NOT NULL,
                    scientific_name VARCHAR(100),
                    category VARCHAR(50) NOT NULL,
                    environment VARCHAR(50) NOT NULL,
                    sun_needs VARCHAR(50) NOT NULL,
                    watering VARCHAR(50) NOT NULL,
                    stock INT NOT NULL DEFAULT 0,
                    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                    image_url TEXT,
                    description TEXT,
                    care_instructions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("OK - Tabela floriculture_plants criada com sucesso")
        else:
            print("OK - Tabela floriculture_plants já existe")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"ERRO - Erro ao criar tabela: {e}")
        return False

def test_plant_creation():
    """Testa a criação de uma planta."""
    try:
        result = create_plant(
            user_id=1,
            name="Rosa de Teste",
            scientific_name="Rosa testensis",
            category="Flores",
            environment="Externo",
            sun_needs="Pleno Sol",
            watering="Diária",
            stock=10,
            price=15.50,
            description="Planta de teste",
            care_instructions="Cuidados de teste"
        )
        
        if result:
            print(f"OK - Planta criada com sucesso: ID {result['id']}")
            return True
        else:
            print("ERRO - Falha ao criar planta")
            return False
    except Exception as e:
        print(f"ERRO - Erro ao criar planta: {e}")
        return False

def main():
    """Função principal do teste."""
    print("Iniciando testes do banco de dados de floricultura...")
    print("-" * 50)
    
    # Teste 1: Conexão com banco
    if not test_database_connection():
        print("Falha na conexão. Abortando testes.")
        return
    
    # Teste 2: Criação da tabela
    if not create_floriculture_plants_table():
        print("Falha na criação da tabela. Abortando testes.")
        return
    
    # Teste 3: Criação de planta
    if not test_plant_creation():
        print("Falha na criação de planta.")
        return
    
    print("-" * 50)
    print("Todos os testes passaram! O sistema está funcionando.")

if __name__ == "__main__":
    main()