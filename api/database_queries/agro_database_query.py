import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class AgroDatabase:
    def __init__(self):
        self.connection = None
        self.connect()
    
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
    
    # Métodos para Animais
    def create_animal(self, official_id, name, birth_date, breed, gender, status, entry_date=None):
        """Cria um novo animal no banco de dados"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        if entry_date is None:
            entry_date = datetime.now()
        
        query = """
        INSERT INTO animals (official_id, name, birth_date, breed, gender, status, entry_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (official_id, name, birth_date, breed, gender, status, entry_date))
            self.connection.commit()
            animal_id = cursor.lastrowid
            return animal_id
        except Error as e:
            print(f"Erro ao criar animal: {e}")
            return None
        finally:
            cursor.close()
    
    def get_animals(self):
        """Obtém todos os animais ativos"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT * FROM animals
        WHERE status != 'Inativo'
        ORDER BY name
        """
        
        try:
            cursor.execute(query)
            animals = cursor.fetchall()
            return animals
        except Error as e:
            print(f"Erro ao obter animais: {e}")
            return None
        finally:
            cursor.close()
    
    def get_animal(self, animal_id):
        """Obtém um animal pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT * FROM animals
        WHERE animal_id = %s
        """
        
        try:
            cursor.execute(query, (animal_id,))
            animal = cursor.fetchone()
            return animal
        except Error as e:
            print(f"Erro ao obter animal: {e}")
            return None
        finally:
            cursor.close()
    
    def update_animal(self, animal_id, official_id, name, birth_date, breed, gender, status, entry_date):
        """Atualiza um animal existente"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        UPDATE animals
        SET official_id = %s, name = %s, birth_date = %s, breed = %s, gender = %s, status = %s, entry_date = %s
        WHERE animal_id = %s
        """
        
        try:
            cursor.execute(query, (official_id, name, birth_date, breed, gender, status, entry_date, animal_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao atualizar animal: {e}")
            return False
        finally:
            cursor.close()
    
    def delete_animal(self, animal_id):
        """Inativa um animal (não exclui do banco)"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        UPDATE animals
        SET status = 'Inativo'
        WHERE animal_id = %s
        """
        
        try:
            cursor.execute(query, (animal_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao inativar animal: {e}")
            return False
        finally:
            cursor.close()
    
    # Métodos para Produção de Leite
    def create_milk_production_entry(self, animal_id, production_date, quantity, period, notes=None):
        """Cria um novo registro de produção de leite"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO milk_production_entries (animal_id, production_date, quantity, period, notes)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (animal_id, production_date, quantity, period, notes))
            self.connection.commit()
            entry_id = cursor.lastrowid
            return entry_id
        except Error as e:
            print(f"Erro ao criar registro de produção: {e}")
            return None
        finally:
            cursor.close()
    
    def count_milk_production_entries(self, animal_id=None, start_date=None, end_date=None):
        """Conta o número total de registros de produção de leite com filtros opcionais"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        SELECT COUNT(*) FROM milk_production_entries e
        WHERE 1=1
        """
        params = []
        
        if animal_id:
            query += " AND e.animal_id = %s"
            params.append(animal_id)
        
        if start_date:
            query += " AND e.production_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND e.production_date <= %s"
            params.append(end_date)
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar registros de produção: {e}")
            return 0
        finally:
            cursor.close()
    
    def get_milk_production_entries(self, page=1, page_size=10, animal_id=None, start_date=None, end_date=None):
        """Obtém registros de produção de leite com paginação e filtros opcionais"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        offset = (page - 1) * page_size
        
        query = """
        SELECT e.*, a.name as animal_name, a.official_id as animal_official_id
        FROM milk_production_entries e
        JOIN animals a ON e.animal_id = a.animal_id
        WHERE 1=1
        """
        params = []
        
        if animal_id:
            query += " AND e.animal_id = %s"
            params.append(animal_id)
        
        if start_date:
            query += " AND e.production_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND e.production_date <= %s"
            params.append(end_date)
        
        query += " ORDER BY e.production_date DESC, e.period ASC LIMIT %s OFFSET %s"
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            entries = cursor.fetchall()
            return entries
        except Error as e:
            print(f"Erro ao obter registros de produção: {e}")
            return None
        finally:
            cursor.close()
    
    def get_milk_production_entry(self, entry_id):
        """Obtém um registro de produção de leite pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT e.*, a.name as animal_name, a.official_id as animal_official_id
        FROM milk_production_entries e
        JOIN animals a ON e.animal_id = a.animal_id
        WHERE e.id = %s
        """
        
        try:
            cursor.execute(query, (entry_id,))
            entry = cursor.fetchone()
            return entry
        except Error as e:
            print(f"Erro ao obter registro de produção: {e}")
            return None
        finally:
            cursor.close()
    
    def update_milk_production_entry(self, entry_id, quantity=None, period=None, notes=None):
        """Atualiza um registro de produção de leite existente"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Obtém os valores atuais
        current = self.get_milk_production_entry(entry_id)
        if not current:
            return False
        
        # Usa os valores atuais se os novos não forem fornecidos
        quantity = quantity if quantity is not None else current['quantity']
        period = period if period is not None else current['period']
        notes = notes if notes is not None else current['notes']
        
        query = """
        UPDATE milk_production_entries
        SET quantity = %s, period = %s, notes = %s
        WHERE id = %s
        """
        
        try:
            cursor.execute(query, (quantity, period, notes, entry_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao atualizar registro de produção: {e}")
            return False
        finally:
            cursor.close()
            
    def delete_milk_production_entry(self, entry_id):
        """Exclui um registro de produção de leite"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        DELETE FROM milk_production_entries
        WHERE id = %s
        """
        
        try:
            cursor.execute(query, (entry_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao excluir registro de produção: {e}")
            return False
        finally:
            cursor.close()
    
    def get_daily_milk_production(self, start_date=None, end_date=None):
        """Obtém a produção diária de leite para o período especificado"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Constrói a consulta com filtros
        query = """
        SELECT production_date as date, SUM(quantity) as total_liters
        FROM milk_production_entries
        WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND production_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND production_date <= %s"
            params.append(end_date)
        
        query += " GROUP BY production_date ORDER BY production_date"
        
        try:
            cursor.execute(query, params)
            daily_production = cursor.fetchall()
            return daily_production
        except Error as e:
            print(f"Erro ao obter produção diária: {e}")
            return []
        finally:
            cursor.close()
    
    def get_milk_production_by_animal(self):
        """Obtém a produção total de leite por animal"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT a.animal_id, a.name as animal_name, SUM(e.quantity) as total_liters
        FROM milk_production_entries e
        JOIN animals a ON e.animal_id = a.animal_id
        GROUP BY a.animal_id, a.name
        ORDER BY total_liters DESC
        """
        
        try:
            cursor.execute(query)
            animal_production = cursor.fetchall()
            return animal_production
        except Error as e:
            print(f"Erro ao obter produção por animal: {e}")
            return []
        finally:
            cursor.close()
    
    # Métodos para compatibilidade
    def get_crop_production_summary(self):
        """Método simulado para compatibilidade"""
        return None
    
    def get_milk_production_monthly(self):
        """Método simulado para compatibilidade"""
        return None
    
    def get_inputs_distribution(self):
        """Método simulado para compatibilidade"""
        return None
    
    def get_soil_ph_by_plot(self):
        """Método simulado para compatibilidade"""
        return None
    
    def get_financial_summary(self):
        """Método simulado para compatibilidade"""
        return None

# Instância global do banco de dados
agro_db = AgroDatabase()