"""
Script para criar as tabelas do banco de dados.
"""

from init_db import init_database

if __name__ == "__main__":
    print("Iniciando criação das tabelas do banco de dados...")
    init_database()
    print("Processo concluído.")