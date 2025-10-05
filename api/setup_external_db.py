#!/usr/bin/env python3
"""
Script para configurar tabelas no banco externo.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.connection import get_db_connection

def create_tables():
    """Cria tabelas necessárias no banco externo."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
        
        # Criar tabela landscaping_projects
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS landscaping_projects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL DEFAULT 1,
                name VARCHAR(100) NOT NULL,
                client_name VARCHAR(100) NOT NULL,
                project_type VARCHAR(50) NOT NULL,
                area_m2 FLOAT NOT NULL,
                start_date DATE NOT NULL,
                expected_end_date DATE,
                budget FLOAT NOT NULL,
                status VARCHAR(50) DEFAULT 'Em Andamento',
                address TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Inserir usuário padrão se não existir
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role)
                VALUES ('admin', 'admin@kealabs.com', 'hashed_password', 'Administrador', 'admin')
            """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("OK - Tabelas criadas no banco externo")
        return True
        
    except Exception as e:
        print(f"ERRO - {e}")
        return False

if __name__ == "__main__":
    create_tables()