#!/usr/bin/env python3
"""
Script para criar o banco de dados kognia_one se não existir.
"""

import os
import sys
import mysql.connector
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def create_database():
    """Cria o banco de dados kognia_one se não existir."""
    try:
        # Conectar ao MySQL sem especificar banco de dados
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root_password"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        
        cursor = connection.cursor()
        
        # Verificar se o banco existe
        cursor.execute("SHOW DATABASES LIKE 'kognia_one'")
        database_exists = cursor.fetchone()
        
        if not database_exists:
            print("Banco de dados 'kognia_one' não existe. Criando...")
            cursor.execute("CREATE DATABASE kognia_one CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("OK - Banco de dados 'kognia_one' criado com sucesso")
        else:
            print("OK - Banco de dados 'kognia_one' já existe")
        
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as e:
        print(f"ERRO - Erro ao conectar com MySQL: {e}")
        return False
    except Exception as e:
        print(f"ERRO - Erro inesperado: {e}")
        return False

def create_users_table():
    """Cria a tabela users se não existir."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root_password"),
            database=os.getenv("DB_NAME", "kognia_one"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        
        cursor = connection.cursor()
        
        # Criar tabela users se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Inserir usuário padrão se não existir
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        user_exists = cursor.fetchone()[0]
        
        if user_exists == 0:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role)
                VALUES ('admin', 'admin@kognia.com', 'hashed_password', 'Administrador', 'admin')
            """)
            print("OK - Usuário admin criado")
        else:
            print("OK - Usuário admin já existe")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("OK - Tabela users configurada")
        return True
        
    except mysql.connector.Error as e:
        print(f"ERRO - Erro ao criar tabela users: {e}")
        return False

def main():
    """Função principal."""
    print("Configurando banco de dados...")
    print("-" * 40)
    
    # Criar banco de dados
    if not create_database():
        print("ERRO - Falha ao criar banco de dados")
        return
    
    # Criar tabela users
    if not create_users_table():
        print("ERRO - Falha ao criar tabela users")
        return
    
    print("-" * 40)
    print("Banco de dados configurado com sucesso!")

if __name__ == "__main__":
    main()