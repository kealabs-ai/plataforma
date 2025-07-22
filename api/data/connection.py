"""
Módulo para gerenciar conexões com o banco de dados MySQL.
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME"),
    'port': int(os.getenv("DB_PORT")),
}

# Pool de conexões
connection_pool = None

def initialize_connection_pool():
    """
    Inicializa o pool de conexões com o banco de dados.
    """
    global connection_pool
    if connection_pool is None:
        try:
            connection_pool = pooling.MySQLConnectionPool(
                pool_name="kognia_pool",
                pool_size=5,
                **DB_CONFIG
            )
            print("Pool de conexões inicializado com sucesso.")
        except mysql.connector.Error as e:
            print(f"Erro ao inicializar pool de conexões: {e}")
            raise

def get_db_connection():
    """
    Obtém uma conexão do pool.
    """
    global connection_pool
    if connection_pool is None:
        initialize_connection_pool()
    
    try:
        return connection_pool.get_connection()
    except Exception as e:
        print(f"Erro ao obter conexão do pool: {e}")
        # Tentar reinicializar o pool
        initialize_connection_pool()
        return connection_pool.get_connection()

def close_all_connections():
    """
    Fecha todas as conexões no pool.
    """
    global connection_pool
    if connection_pool:
        connection_pool = None
        print("Pool de conexões fechado.")