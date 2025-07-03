import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import date
from typing import List, Dict, Any, Optional

# Carrega variáveis de ambiente
load_dotenv()

class MilkDatabaseQuery:
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
    
    def get_animals_with_production(self, start_date: Optional[date] = None, 
                                   end_date: Optional[date] = None, 
                                   user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtém dados de animais relacionados com produção de leite, filtrados por período e usuário.
        
        Args:
            start_date: Data de início para filtrar registros de produção
            end_date: Data de fim para filtrar registros de produção
            user_id: ID do usuário para filtrar registros de produção
            
        Returns:
            Lista de dicionários com dados de animais e suas produções
        """
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            a.animal_id,
            a.official_id,
            a.name,
            a.birth_date,
            a.breed,
            a.gender,
            a.status,
            a.entry_date,
            mp.id AS production_id,
            mp.production_date,
            mp.liters_produced,
            mp.period,
            mp.notes,
            mp.user_id
        FROM 
            animals a
        JOIN 
            milk_production mp ON a.animal_id = mp.animal_id
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
        
        query += " ORDER BY mp.production_date DESC"
        
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Formatar datas para strings ISO
            for row in results:
                if row.get('birth_date'):
                    row['birth_date'] = row['birth_date'].isoformat()
                if row.get('entry_date'):
                    row['entry_date'] = row['entry_date'].isoformat()
                if row.get('production_date'):
                    row['production_date'] = row['production_date'].isoformat()
            
            return results
        except Error as e:
            print(f"Erro ao obter animais com produção: {e}")
            return []
        finally:
            cursor.close()

    def get_daily_milk_production(self, start_date: Optional[date] = None, 
                                 end_date: Optional[date] = None,
                                 user_id: Optional[int] = None,
                                 animal_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtém a produção diária de leite para o período especificado, filtrada por usuário e animal.
        
        Args:
            start_date: Data de início para filtrar registros
            end_date: Data de fim para filtrar registros
            user_id: ID do usuário para filtrar registros
            animal_id: ID do animal para filtrar registros
            
        Returns:
            Lista de dicionários com a produção diária
        """
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT 
            mp.production_date AS date,
            SUM(mp.liters_produced) AS total_liters
        FROM 
            milk_production mp
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
        
        query += " GROUP BY mp.production_date ORDER BY mp.production_date"
        
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            daily_production = []
            
            for result in results:
                daily_production.append({
                    'date': result['date'].isoformat() if result['date'] else None,
                    'total_liters': float(result['total_liters']) if result['total_liters'] else 0,
                    'quantity': float(result['total_liters']) if result['total_liters'] else 0
                })
            
            return daily_production
        except Error as e:
            print(f"Erro ao obter produção diária: {e}")
            return []
        finally:
            cursor.close()

    def get_total_milk_production(self, start_date: Optional[date] = None, 
                                 end_date: Optional[date] = None,
                                 user_id: Optional[int] = None,
                                 animal_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Obtém o total de litros de leite produzidos em um período por um usuário.
        
        Args:
            start_date: Data de início para filtrar registros de produção
            end_date: Data de fim para filtrar registros de produção
            user_id: ID do usuário para filtrar registros de produção
            animal_id: ID do animal para filtrar registros de produção
            
        Returns:
            Dicionário com o total de litros produzidos
        """
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT
            SUM(m.liters_produced) AS total_liters
        FROM
            milk_production AS m
        WHERE
            1=1
        """
        
        params = []
        
        if start_date:
            query += " AND m.production_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND m.production_date <= %s"
            params.append(end_date)
        
        if user_id:
            query += " AND m.user_id = %s"
            params.append(user_id)
        
        if animal_id:
            query += " AND m.animal_id = %s"
            params.append(animal_id)
        
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            # Garantir que o resultado seja um número, mesmo se for NULL
            total_liters = float(result['total_liters']) if result and result['total_liters'] else 0.0
            
            return {
                "total_liters": total_liters,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
                "user_id": user_id,
                "animal_id": animal_id
            }
        except Error as e:
            print(f"Erro ao obter total de produção de leite: {e}")
            return {"total_liters": 0.0, "error": str(e)}
        finally:
            cursor.close()

milk_db_query = MilkDatabaseQuery()