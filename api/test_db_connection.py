#!/usr/bin/env python3
"""
Teste de conexão com o banco de dados externo.
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.connection import reset_connection_pool, get_db_connection

def test_connection():
    """Testa conexão com banco externo."""
    try:
        print("Testando conexão com banco externo...")
        print(f"Host: {os.getenv('DB_HOST')}")
        print(f"Port: {os.getenv('DB_PORT')}")
        print(f"User: {os.getenv('DB_USER')}")
        print(f"Database: {os.getenv('DB_NAME')}")
        
        # Resetar pool e tentar conectar
        reset_connection_pool()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        print("OK - Conexão com banco externo OK!")
        return True
        
    except Exception as e:
        print(f"ERRO - Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    test_connection()