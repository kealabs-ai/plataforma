#!/usr/bin/env python3
"""
Inicializa conexão com banco de dados.
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Inicializa conexão com banco de dados."""
    try:
        from data.connection import initialize_connection_pool, test_connection
        
        print("Inicializando conexão com banco de dados...")
        initialize_connection_pool()
        
        success, message = test_connection()
        if success:
            print("✓ Conexão com banco de dados estabelecida")
            return True
        else:
            print(f"✗ Erro na conexão: {message}")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao inicializar banco: {e}")
        return False

if __name__ == "__main__":
    init_database()