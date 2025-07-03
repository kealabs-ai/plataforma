import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import date
from typing import List, Dict, Any, Optional

# Carrega variáveis de ambiente
load_dotenv()

class MilkDatabaseQueryAnimal:
    def __init__(self):
        self.connection = None
        self.connect()
        print("Conectado ao banco de dados sem recriar tabelas")
    
    def connect(self):
        """Conecta ao banco de dados MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "root_password"),
                database=os.getenv("DB_NAME", "kognia_one_db")
            )
            print("Conexão com o banco de dados estabelecida com sucesso")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados MySQL: {e}")
    
    def ensure_connection(self):
        """Garante que a conexão está ativa"""
        if self.connection is None or not self.connection.is_connected():
            self.connect()
    
    def get_daily_milk_production_by_animal(self, start_date: Optional[date] = None, 
                                          end_date: Optional[date] = None,
                                          user_id: Optional[int] = None,
                                          animal_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtém a produção diária de leite por animal para o período especificado.
        
        Args:
            start_date: Data de início para filtrar registros
            end_date: Data de fim para filtrar registros
            user_id: ID do usuário para filtrar registros
            animal_id: ID do animal para filtrar registros
            
        Returns:
            Lista de dicionários com a produção diária por animal
        """
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            mp.production_date AS date,
            mp.animal_id,
            a.name AS animal_name,
            a.official_id,
            SUM(mp.liters_produced) AS total_liters
        FROM 
            milk_production mp
        JOIN
            animals a ON mp.animal_id = a.animal_id
        WHERE 
            1=1
        """
        
        params = []
        
        if start_date:
            query += " AND mp.production_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND mp.production_date <= %s"
            params.append(end_date)
        
        if user_id:
            query += " AND mp.user_id = %s"
            params.append(user_id)
            
        if animal_id:
            query += " AND mp.animal_id = %s"
            params.append(animal_id)
        
        query += " GROUP BY mp.production_date, mp.animal_id, a.name, a.official_id ORDER BY mp.production_date, a.name"
        
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            daily_production = []
            
            for result in results:
                daily_production.append({
                    'date': result['date'].isoformat() if result['date'] else None,
                    'animal_id': result['animal_id'],
                    'animal_name': result['animal_name'] or result['official_id'],
                    'official_id': result['official_id'],
                    'total_liters': float(result['total_liters']) if result['total_liters'] else 0
                })
            
            return daily_production
        except Error as e:
            print(f"Erro ao obter produção diária por animal: {e}")
            return []
        finally:
            cursor.close()

milk_db_query_animal = MilkDatabaseQueryAnimal()