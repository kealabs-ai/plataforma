"""
Script para inicializar o banco de dados e criar as tabelas necessárias.
"""

import os
import mysql.connector
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', '3306')),
}

DB_NAME = os.getenv('DB_NAME', 'kognia_one')

def create_database():
    """
    Cria o banco de dados se não existir.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Banco de dados '{DB_NAME}' criado ou já existente.")
    except Exception as e:
        print(f"Erro ao criar banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

def execute_sql_file(file_path):
    """
    Executa um arquivo SQL.
    """
    conn = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
    cursor = conn.cursor()
    
    try:
        with open(file_path, 'r') as file:
            sql_commands = file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)
            
            conn.commit()
        print(f"Arquivo SQL '{file_path}' executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar arquivo SQL '{file_path}': {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def init_database():
    """
    Inicializa o banco de dados e cria todas as tabelas necessárias.
    """
    # Criar o banco de dados
    create_database()
    
    # Diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Executar arquivos SQL
    schema_files = [
        os.path.join(current_dir, "floriculture_schema.sql"),
        os.path.join(current_dir, "landscaping_schema.sql")
    ]
    
    for file_path in schema_files:
        if os.path.exists(file_path):
            execute_sql_file(file_path)
        else:
            print(f"Arquivo '{file_path}' não encontrado.")

if __name__ == "__main__":
    init_database()