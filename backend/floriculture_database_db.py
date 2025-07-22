from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
import os
import json
from dotenv import load_dotenv
from data.connection import connection

# Carrega variáveis de ambiente
load_dotenv()

class FloricultureDatabase:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Conecta ao banco de dados MySQL"""
        try:
            self.connection = connection.DB_CONFIG

            print("Conexão com o banco de dados estabelecida com sucesso")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados MySQL: {e}")
    
    def ensure_connection(self):
        """Garante que a conexão está ativa"""
        if self.connection is None or not self.connection.is_connected():
            self.connect()
    
    # ===== Operações CRUD para Cultivo de Flores =====
    
    def create_flower_cultivation(self, user_id, species, variety, planting_date, quantity, area_m2, 
                                 greenhouse_id=None, expected_harvest_date=None, status="Em Cultivo", notes=None):
        """Cria um novo registro de cultivo de flores"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO flower_cultivation 
        (user_id, species, variety, planting_date, quantity, area_m2, greenhouse_id, expected_harvest_date, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (user_id, species, variety, planting_date, quantity, area_m2, 
                                  greenhouse_id, expected_harvest_date, status, notes))
            self.connection.commit()
            flower_id = cursor.lastrowid
            
            # Registrar atividade do usuário
            details = {
                "action": "create",
                "species": species,
                "variety": variety,
                "quantity": quantity
            }
            self.create_user_activity(user_id, "cultivation", flower_id, details)
            
            return self.get_flower_cultivation(flower_id)
        except Error as e:
            print(f"Erro ao criar cultivo de flores: {e}")
            return None
        finally:
            cursor.close()
    
    def get_flower_cultivation(self, flower_id):
        """Obtém um cultivo de flores pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT f.*, g.name as greenhouse_name
        FROM flower_cultivation f
        LEFT JOIN greenhouses g ON f.greenhouse_id = g.id
        WHERE f.id = %s
        """
        
        try:
            cursor.execute(query, (flower_id,))
            flower = cursor.fetchone()
            return flower
        except Error as e:
            print(f"Erro ao obter cultivo de flores: {e}")
            return None
        finally:
            cursor.close()
    
    def get_all_flower_cultivations(self, filters=None, page=1, page_size=10):
        """Obtém todos os cultivos de flores com filtros e paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = """
        SELECT f.*, g.name as greenhouse_name
        FROM flower_cultivation f
        LEFT JOIN greenhouses g ON f.greenhouse_id = g.id
        WHERE 1=1
        """
        params = []
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'species' in filters and filters['species']:
                query += " AND f.species LIKE %s"
                params.append(f"%{filters['species']}%")
            
            if 'status' in filters and filters['status']:
                query += " AND f.status = %s"
                params.append(filters['status'])
            
            if 'greenhouse_id' in filters and filters['greenhouse_id']:
                query += " AND f.greenhouse_id = %s"
                params.append(filters['greenhouse_id'])
            
            if 'user_id' in filters and filters['user_id']:
                query += " AND f.user_id = %s"
                params.append(filters['user_id'])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY f.planting_date DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            flowers = cursor.fetchall()
            return flowers
        except Error as e:
            print(f"Erro ao obter cultivos de flores: {e}")
            return []
        finally:
            cursor.close()
    
    def count_flower_cultivations(self, filters=None):
        """Conta o número total de cultivos de flores com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM flower_cultivation f WHERE 1=1"
        params = []
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'species' in filters and filters['species']:
                query += " AND f.species LIKE %s"
                params.append(f"%{filters['species']}%")
            
            if 'status' in filters and filters['status']:
                query += " AND f.status = %s"
                params.append(filters['status'])
            
            if 'greenhouse_id' in filters and filters['greenhouse_id']:
                query += " AND f.greenhouse_id = %s"
                params.append(filters['greenhouse_id'])
            
            if 'user_id' in filters and filters['user_id']:
                query += " AND f.user_id = %s"
                params.append(filters['user_id'])
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar cultivos de flores: {e}")
            return 0
        finally:
            cursor.close()
    
    def update_flower_cultivation(self, flower_id, user_id, update_data):
        """Atualiza um cultivo de flores"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o cultivo existe e pertence ao usuário
        flower = self.get_flower_cultivation(flower_id)
        if not flower or flower['user_id'] != user_id:
            return None
        
        # Construir a consulta de atualização
        query = "UPDATE flower_cultivation SET "
        params = []
        
        # Adicionar campos a serem atualizados
        update_fields = []
        for key, value in update_data.items():
            if key in ['species', 'variety', 'planting_date', 'quantity', 'area_m2', 
                      'greenhouse_id', 'expected_harvest_date', 'status', 'notes']:
                update_fields.append(f"{key} = %s")
                params.append(value)
        
        if not update_fields:
            return flower  # Nada para atualizar
        
        query += ", ".join(update_fields)
        query += ", updated_at = NOW() WHERE id = %s"
        params.append(flower_id)
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            
            # Registrar atividade do usuário
            details = {
                "action": "update",
                "updated_fields": list(update_data.keys())
            }
            self.create_user_activity(user_id, "cultivation", flower_id, details)
            
            return self.get_flower_cultivation(flower_id)
        except Error as e:
            print(f"Erro ao atualizar cultivo de flores: {e}")
            return None
        finally:
            cursor.close()
    
    def delete_flower_cultivation(self, flower_id, user_id):
        """Exclui um cultivo de flores"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o cultivo existe e pertence ao usuário
        flower = self.get_flower_cultivation(flower_id)
        if not flower or flower['user_id'] != user_id:
            return False
        
        query = "DELETE FROM flower_cultivation WHERE id = %s"
        
        try:
            cursor.execute(query, (flower_id,))
            self.connection.commit()
            
            # Registrar atividade do usuário
            details = {
                "action": "delete",
                "species": flower['species'],
                "variety": flower['variety']
            }
            self.create_user_activity(user_id, "cultivation", flower_id, details)
            
            return True
        except Error as e:
            print(f"Erro ao excluir cultivo de flores: {e}")
            return False
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Estufas =====
    
    def create_greenhouse(self, user_id, name, area_m2, type, temperature_control=False, 
                         humidity_control=False, irrigation_system=False, location=None, notes=None):
        """Cria uma nova estufa"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO greenhouses 
        (user_id, name, area_m2, type, temperature_control, humidity_control, irrigation_system, location, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (user_id, name, area_m2, type, 
                                  1 if temperature_control else 0, 
                                  1 if humidity_control else 0, 
                                  1 if irrigation_system else 0, 
                                  location, notes))
            self.connection.commit()
            greenhouse_id = cursor.lastrowid
            
            # Registrar atividade do usuário
            details = {
                "action": "create",
                "name": name,
                "type": type,
                "area_m2": area_m2
            }
            self.create_user_activity(user_id, "greenhouse", greenhouse_id, details)
            
            return self.get_greenhouse(greenhouse_id)
        except Error as e:
            print(f"Erro ao criar estufa: {e}")
            return None
        finally:
            cursor.close()
    
    def get_greenhouse(self, greenhouse_id):
        """Obtém uma estufa pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = "SELECT * FROM greenhouses WHERE id = %s"
        
        try:
            cursor.execute(query, (greenhouse_id,))
            greenhouse = cursor.fetchone()
            
            # Converter valores TINYINT para booleanos
            if greenhouse:
                greenhouse['temperature_control'] = bool(greenhouse['temperature_control'])
                greenhouse['humidity_control'] = bool(greenhouse['humidity_control'])
                greenhouse['irrigation_system'] = bool(greenhouse['irrigation_system'])
            
            return greenhouse
        except Error as e:
            print(f"Erro ao obter estufa: {e}")
            return None
        finally:
            cursor.close()
    
    def get_all_greenhouses(self, filters=None, page=1, page_size=10):
        """Obtém todas as estufas com filtros e paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = "SELECT * FROM greenhouses WHERE 1=1"
        params = []
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'type' in filters and filters['type']:
                query += " AND type LIKE %s"
                params.append(f"%{filters['type']}%")
            
            if 'user_id' in filters and filters['user_id']:
                query += " AND user_id = %s"
                params.append(filters['user_id'])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY name ASC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            greenhouses = cursor.fetchall()
            
            # Converter valores TINYINT para booleanos
            for greenhouse in greenhouses:
                greenhouse['temperature_control'] = bool(greenhouse['temperature_control'])
                greenhouse['humidity_control'] = bool(greenhouse['humidity_control'])
                greenhouse['irrigation_system'] = bool(greenhouse['irrigation_system'])
            
            return greenhouses
        except Error as e:
            print(f"Erro ao obter estufas: {e}")
            return []
        finally:
            cursor.close()
    
    def count_greenhouses(self, filters=None):
        """Conta o número total de estufas com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM greenhouses WHERE 1=1"
        params = []
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'type' in filters and filters['type']:
                query += " AND type LIKE %s"
                params.append(f"%{filters['type']}%")
            
            if 'user_id' in filters and filters['user_id']:
                query += " AND user_id = %s"
                params.append(filters['user_id'])
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar estufas: {e}")
            return 0
        finally:
            cursor.close()
    
    def update_greenhouse(self, greenhouse_id, user_id, update_data):
        """Atualiza uma estufa"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se a estufa existe e pertence ao usuário
        greenhouse = self.get_greenhouse(greenhouse_id)
        if not greenhouse or greenhouse['user_id'] != user_id:
            return None
        
        # Construir a consulta de atualização
        query = "UPDATE greenhouses SET "
        params = []
        
        # Adicionar campos a serem atualizados
        update_fields = []
        for key, value in update_data.items():
            if key in ['name', 'area_m2', 'type', 'location', 'notes']:
                update_fields.append(f"{key} = %s")
                params.append(value)
            elif key in ['temperature_control', 'humidity_control', 'irrigation_system']:
                update_fields.append(f"{key} = %s")
                params.append(1 if value else 0)
        
        if not update_fields:
            return greenhouse  # Nada para atualizar
        
        query += ", ".join(update_fields)
        query += ", updated_at = NOW() WHERE id = %s"
        params.append(greenhouse_id)
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            
            # Registrar atividade do usuário
            details = {
                "action": "update",
                "updated_fields": list(update_data.keys())
            }
            self.create_user_activity(user_id, "greenhouse", greenhouse_id, details)
            
            return self.get_greenhouse(greenhouse_id)
        except Error as e:
            print(f"Erro ao atualizar estufa: {e}")
            return None
        finally:
            cursor.close()
    
    def delete_greenhouse(self, greenhouse_id, user_id):
        """Exclui uma estufa"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se a estufa existe e pertence ao usuário
        greenhouse = self.get_greenhouse(greenhouse_id)
        if not greenhouse or greenhouse['user_id'] != user_id:
            return False
        
        query = "DELETE FROM greenhouses WHERE id = %s"
        
        try:
            cursor.execute(query, (greenhouse_id,))
            self.connection.commit()
            
            # Registrar atividade do usuário
            details = {
                "action": "delete",
                "name": greenhouse['name'],
                "type": greenhouse['type']
            }
            self.create_user_activity(user_id, "greenhouse", greenhouse_id, details)
            
            return True
        except Error as e:
            print(f"Erro ao excluir estufa: {e}")
            return False
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Registros de Clima =====
    
    def create_climate_record(self, greenhouse_id, user_id, record_date, record_time, 
                             temperature, humidity, light_level=None, notes=None):
        """Cria um novo registro de clima"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO greenhouse_climate_records 
        (greenhouse_id, user_id, record_date, record_time, temperature, humidity, light_level, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (greenhouse_id, user_id, record_date, record_time, 
                                  temperature, humidity, light_level, notes))
            self.connection.commit()
            record_id = cursor.lastrowid
            
            # Registrar atividade do usuário
            details = {
                "action": "create",
                "greenhouse_id": greenhouse_id,
                "temperature": temperature,
                "humidity": humidity
            }
            self.create_user_activity(user_id, "climate", record_id, details)
            
            return self.get_climate_record(record_id)
        except Error as e:
            print(f"Erro ao criar registro de clima: {e}")
            return None
        finally:
            cursor.close()
    
    def get_climate_record(self, record_id):
        """Obtém um registro de clima pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT c.*, g.name as greenhouse_name
        FROM greenhouse_climate_records c
        JOIN greenhouses g ON c.greenhouse_id = g.id
        WHERE c.id = %s
        """
        
        try:
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
            return record
        except Error as e:
            print(f"Erro ao obter registro de clima: {e}")
            return None
        finally:
            cursor.close()
    
    def get_climate_records(self, greenhouse_id, page=1, page_size=10, start_date=None, end_date=None):
        """Obtém registros de clima para uma estufa específica com paginação e filtros de data"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = """
        SELECT c.*, g.name as greenhouse_name
        FROM greenhouse_climate_records c
        JOIN greenhouses g ON c.greenhouse_id = g.id
        WHERE c.greenhouse_id = %s
        """
        params = [greenhouse_id]
        
        # Adicionar filtros de data se fornecidos
        if start_date:
            query += " AND c.record_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND c.record_date <= %s"
            params.append(end_date)
        
        # Adicionar ordenação e paginação
        query += " ORDER BY c.record_date DESC, c.record_time DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Erro ao obter registros de clima: {e}")
            return []
        finally:
            cursor.close()
    
    def count_climate_records(self, greenhouse_id, start_date=None, end_date=None):
        """Conta o número total de registros de clima para uma estufa específica com filtros de data"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM greenhouse_climate_records WHERE greenhouse_id = %s"
        params = [greenhouse_id]
        
        # Adicionar filtros de data se fornecidos
        if start_date:
            query += " AND record_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND record_date <= %s"
            params.append(end_date)
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar registros de clima: {e}")
            return 0
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Registros de Colheita =====
    
    def create_harvest_record(self, flower_id, user_id, harvest_date, quantity, quality_grade, notes=None):
        """Cria um novo registro de colheita"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO flower_harvest_records 
        (flower_id, user_id, harvest_date, quantity, quality_grade, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (flower_id, user_id, harvest_date, quantity, quality_grade, notes))
            self.connection.commit()
            record_id = cursor.lastrowid
            
            # Registrar atividade do usuário
            details = {
                "action": "create",
                "flower_id": flower_id,
                "quantity": quantity,
                "quality_grade": quality_grade
            }
            self.create_user_activity(user_id, "harvest", record_id, details)
            
            return self.get_harvest_record(record_id)
        except Error as e:
            print(f"Erro ao criar registro de colheita: {e}")
            return None
        finally:
            cursor.close()
    
    def get_harvest_record(self, record_id):
        """Obtém um registro de colheita pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT h.*, f.species, f.variety
        FROM flower_harvest_records h
        JOIN flower_cultivation f ON h.flower_id = f.id
        WHERE h.id = %s
        """
        
        try:
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
            return record
        except Error as e:
            print(f"Erro ao obter registro de colheita: {e}")
            return None
        finally:
            cursor.close()
    
    def get_harvest_records(self, flower_id, page=1, page_size=10):
        """Obtém registros de colheita para um cultivo específico com paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT h.*, f.species, f.variety
        FROM flower_harvest_records h
        JOIN flower_cultivation f ON h.flower_id = f.id
        WHERE h.flower_id = %s
        ORDER BY h.harvest_date DESC
        LIMIT %s OFFSET %s
        """
        
        offset = (page - 1) * page_size
        
        try:
            cursor.execute(query, (flower_id, page_size, offset))
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Erro ao obter registros de colheita: {e}")
            return []
        finally:
            cursor.close()
    
    def count_harvest_records(self, flower_id):
        """Conta o número total de registros de colheita para um cultivo específico"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = "SELECT COUNT(*) FROM flower_harvest_records WHERE flower_id = %s"
        
        try:
            cursor.execute(query, (flower_id,))
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar registros de colheita: {e}")
            return 0
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Registros de Tratamento =====
    
    def create_treatment_record(self, flower_id, user_id, treatment_date, treatment_type, 
                              product_used, quantity, unit, notes=None):
        """Cria um novo registro de tratamento"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO flower_treatment_records 
        (flower_id, user_id, treatment_date, treatment_type, product_used, quantity, unit, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (flower_id, user_id, treatment_date, treatment_type, 
                                  product_used, quantity, unit, notes))
            self.connection.commit()
            record_id = cursor.lastrowid
            
            # Registrar atividade do usuário
            details = {
                "action": "create",
                "flower_id": flower_id,
                "treatment_type": treatment_type,
                "product_used": product_used
            }
            self.create_user_activity(user_id, "treatment", record_id, details)
            
            return self.get_treatment_record(record_id)
        except Error as e:
            print(f"Erro ao criar registro de tratamento: {e}")
            return None
        finally:
            cursor.close()
    
    def get_treatment_record(self, record_id):
        """Obtém um registro de tratamento pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT t.*, f.species, f.variety
        FROM flower_treatment_records t
        JOIN flower_cultivation f ON t.flower_id = f.id
        WHERE t.id = %s
        """
        
        try:
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
            return record
        except Error as e:
            print(f"Erro ao obter registro de tratamento: {e}")
            return None
        finally:
            cursor.close()
    
    def get_treatment_records(self, flower_id, page=1, page_size=10, treatment_type=None):
        """Obtém registros de tratamento para um cultivo específico com paginação e filtro de tipo"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = """
        SELECT t.*, f.species, f.variety
        FROM flower_treatment_records t
        JOIN flower_cultivation f ON t.flower_id = f.id
        WHERE t.flower_id = %s
        """
        params = [flower_id]
        
        # Adicionar filtro de tipo se fornecido
        if treatment_type:
            query += " AND t.treatment_type = %s"
            params.append(treatment_type)
        
        # Adicionar ordenação e paginação
        query += " ORDER BY t.treatment_date DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Erro ao obter registros de tratamento: {e}")
            return []
        finally:
            cursor.close()
    
    def count_treatment_records(self, flower_id, treatment_type=None):
        """Conta o número total de registros de tratamento para um cultivo específico com filtro de tipo"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM flower_treatment_records WHERE flower_id = %s"
        params = [flower_id]
        
        # Adicionar filtro de tipo se fornecido
        if treatment_type:
            query += " AND treatment_type = %s"
            params.append(treatment_type)
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar registros de tratamento: {e}")
            return 0
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Registros de Venda =====
    
    def create_sale_record(self, flower_id, user_id, sale_date, quantity, price_per_unit, 
                          total_value=None, buyer=None, notes=None):
        """Cria um novo registro de venda"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Calcular o valor total se não fornecido
        if total_value is None:
            total_value = quantity * price_per_unit
        
        query = """
        INSERT INTO flower_sale_records 
        (flower_id, user_id, sale_date, quantity, price_per_unit, total_value, buyer, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (flower_id, user_id, sale_date, quantity, 
                                  price_per_unit, total_value, buyer, notes))
            self.connection.commit()
            record_id = cursor.lastrowid
            
            # Registrar atividade do usuário
            details = {
                "action": "create",
                "flower_id": flower_id,
                "quantity": quantity,
                "total_value": total_value
            }
            self.create_user_activity(user_id, "sale", record_id, details)
            
            return self.get_sale_record(record_id)
        except Error as e:
            print(f"Erro ao criar registro de venda: {e}")
            return None
        finally:
            cursor.close()
    
    def get_sale_record(self, record_id):
        """Obtém um registro de venda pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT s.*, f.species, f.variety
        FROM flower_sale_records s
        JOIN flower_cultivation f ON s.flower_id = f.id
        WHERE s.id = %s
        """
        
        try:
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
            return record
        except Error as e:
            print(f"Erro ao obter registro de venda: {e}")
            return None
        finally:
            cursor.close()
    
    def get_sale_records(self, page=1, page_size=10, start_date=None, end_date=None, flower_id=None):
        """Obtém registros de venda com paginação e filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = """
        SELECT s.*, f.species, f.variety
        FROM flower_sale_records s
        JOIN flower_cultivation f ON s.flower_id = f.id
        WHERE 1=1
        """
        params = []
        
        # Adicionar filtros se fornecidos
        if flower_id:
            query += " AND s.flower_id = %s"
            params.append(flower_id)
        
        if start_date:
            query += " AND s.sale_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND s.sale_date <= %s"
            params.append(end_date)
        
        # Adicionar ordenação e paginação
        query += " ORDER BY s.sale_date DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Erro ao obter registros de venda: {e}")
            return []
        finally:
            cursor.close()
    
    def count_sale_records(self, start_date=None, end_date=None, flower_id=None):
        """Conta o número total de registros de venda com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM flower_sale_records WHERE 1=1"
        params = []
        
        # Adicionar filtros se fornecidos
        if flower_id:
            query += " AND flower_id = %s"
            params.append(flower_id)
        
        if start_date:
            query += " AND sale_date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND sale_date <= %s"
            params.append(end_date)
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar registros de venda: {e}")
            return 0
        finally:
            cursor.close()
    
    # ===== Operações para Preferências do Usuário =====
    
    def get_user_preferences(self, user_id):
        """Obtém as preferências do usuário"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = "SELECT * FROM user_floriculture_preferences WHERE user_id = %s"
        
        try:
            cursor.execute(query, (user_id,))
            preferences = cursor.fetchone()
            
            # Converter strings JSON para objetos Python
            if preferences:
                if preferences['preferred_flowers']:
                    preferences['preferred_flowers'] = json.loads(preferences['preferred_flowers'])
                if preferences['dashboard_layout']:
                    preferences['dashboard_layout'] = json.loads(preferences['dashboard_layout'])
            
            return preferences
        except Error as e:
            print(f"Erro ao obter preferências do usuário: {e}")
            return None
        finally:
            cursor.close()
    
    def update_user_preferences(self, user_id, preferences_data):
        """Atualiza ou cria as preferências do usuário"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o usuário já tem preferências
        existing_preferences = self.get_user_preferences(user_id)
        
        if existing_preferences:
            # Atualizar preferências existentes
            query = "UPDATE user_floriculture_preferences SET "
            params = []
            
            # Adicionar campos a serem atualizados
            update_fields = []
            
            if 'preferred_flowers' in preferences_data:
                update_fields.append("preferred_flowers = %s")
                params.append(json.dumps(preferences_data['preferred_flowers']))
            
            if 'preferred_notification_method' in preferences_data:
                update_fields.append("preferred_notification_method = %s")
                params.append(preferences_data['preferred_notification_method'])
            
            if 'notification_frequency' in preferences_data:
                update_fields.append("notification_frequency = %s")
                params.append(preferences_data['notification_frequency'])
            
            if 'dashboard_layout' in preferences_data:
                update_fields.append("dashboard_layout = %s")
                params.append(json.dumps(preferences_data['dashboard_layout']))
            
            if not update_fields:
                return existing_preferences  # Nada para atualizar
            
            query += ", ".join(update_fields)
            query += ", updated_at = NOW() WHERE user_id = %s"
            params.append(user_id)
            
            try:
                cursor.execute(query, params)
                self.connection.commit()
                return self.get_user_preferences(user_id)
            except Error as e:
                print(f"Erro ao atualizar preferências do usuário: {e}")
                return None
            finally:
                cursor.close()
        else:
            # Criar novas preferências
            preferred_flowers = json.dumps(preferences_data.get('preferred_flowers', []))
            preferred_notification_method = preferences_data.get('preferred_notification_method', 'email')
            notification_frequency = preferences_data.get('notification_frequency', 'daily')
            dashboard_layout = json.dumps(preferences_data.get('dashboard_layout', {}))
            
            query = """
            INSERT INTO user_floriculture_preferences 
            (user_id, preferred_flowers, preferred_notification_method, notification_frequency, dashboard_layout)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            try:
                cursor.execute(query, (user_id, preferred_flowers, preferred_notification_method, 
                                      notification_frequency, dashboard_layout))
                self.connection.commit()
                return self.get_user_preferences(user_id)
            except Error as e:
                print(f"Erro ao criar preferências do usuário: {e}")
                return None
            finally:
                cursor.close()
    
    # ===== Operações para Atividades do Usuário =====
    
    def create_user_activity(self, user_id, activity_type, activity_id, details=None):
        """Registra uma atividade do usuário"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        details_json = json.dumps(details) if details else None
        
        query = """
        INSERT INTO user_floriculture_activities 
        (user_id, activity_type, activity_id, details)
        VALUES (%s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (user_id, activity_type, activity_id, details_json))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erro ao registrar atividade do usuário: {e}")
            return None
        finally:
            cursor.close()
    
    def get_user_activities(self, user_id, page=1, page_size=10, activity_type=None, start_date=None, end_date=None):
        """Obtém atividades do usuário com paginação e filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = "SELECT * FROM user_floriculture_activities WHERE user_id = %s"
        params = [user_id]
        
        # Adicionar filtros se fornecidos
        if activity_type:
            query += " AND activity_type = %s"
            params.append(activity_type)
        
        if start_date:
            query += " AND DATE(timestamp) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(timestamp) <= %s"
            params.append(end_date)
        
        # Adicionar ordenação e paginação
        query += " ORDER BY timestamp DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            activities = cursor.fetchall()
            
            # Converter strings JSON para objetos Python
            for activity in activities:
                if activity['details']:
                    activity['details'] = json.loads(activity['details'])
            
            return activities
        except Error as e:
            print(f"Erro ao obter atividades do usuário: {e}")
            return []
        finally:
            cursor.close()
    
    def count_user_activities(self, user_id, activity_type=None, start_date=None, end_date=None):
        """Conta o número total de atividades do usuário com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM user_floriculture_activities WHERE user_id = %s"
        params = [user_id]
        
        # Adicionar filtros se fornecidos
        if activity_type:
            query += " AND activity_type = %s"
            params.append(activity_type)
        
        if start_date:
            query += " AND DATE(timestamp) >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(timestamp) <= %s"
            params.append(end_date)
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar atividades do usuário: {e}")
            return 0
        finally:
            cursor.close()
    
    # ===== Operações para Notificações do Usuário =====
    
    def create_notification(self, user_id, title, message, notification_type, 
                           related_entity_type=None, related_entity_id=None):
        """Cria uma nova notificação para o usuário"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO user_floriculture_notifications 
        (user_id, title, message, notification_type, related_entity_type, related_entity_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (user_id, title, message, notification_type, 
                                  related_entity_type, related_entity_id))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erro ao criar notificação: {e}")
            return None
        finally:
            cursor.close()
    
    def get_user_notifications(self, user_id, page=1, page_size=10, is_read=None, notification_type=None):
        """Obtém notificações do usuário com paginação e filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = "SELECT * FROM user_floriculture_notifications WHERE user_id = %s"
        params = [user_id]
        
        # Adicionar filtros se fornecidos
        if is_read is not None:
            query += " AND is_read = %s"
            params.append(1 if is_read else 0)
        
        if notification_type:
            query += " AND notification_type = %s"
            params.append(notification_type)
        
        # Adicionar ordenação e paginação
        query += " ORDER BY created_at DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            notifications = cursor.fetchall()
            
            # Converter valores TINYINT para booleanos
            for notification in notifications:
                notification['is_read'] = bool(notification['is_read'])
            
            return notifications
        except Error as e:
            print(f"Erro ao obter notificações do usuário: {e}")
            return []
        finally:
            cursor.close()
    
    def count_user_notifications(self, user_id, is_read=None, notification_type=None):
        """Conta o número total de notificações do usuário com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM user_floriculture_notifications WHERE user_id = %s"
        params = [user_id]
        
        # Adicionar filtros se fornecidos
        if is_read is not None:
            query += " AND is_read = %s"
            params.append(1 if is_read else 0)
        
        if notification_type:
            query += " AND notification_type = %s"
            params.append(notification_type)
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar notificações do usuário: {e}")
            return 0
        finally:
            cursor.close()
    
    def mark_notification_as_read(self, notification_id, user_id):
        """Marca uma notificação como lida"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = "UPDATE user_floriculture_notifications SET is_read = 1 WHERE id = %s AND user_id = %s"
        
        try:
            cursor.execute(query, (notification_id, user_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Erro ao marcar notificação como lida: {e}")
            return False
        finally:
            cursor.close()
    
    def mark_all_notifications_as_read(self, user_id):
        """Marca todas as notificações do usuário como lidas"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = "UPDATE user_floriculture_notifications SET is_read = 1 WHERE user_id = %s AND is_read = 0"
        
        try:
            cursor.execute(query, (user_id,))
            self.connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Erro ao marcar todas as notificações como lidas: {e}")
            return 0
        finally:
            cursor.close()
    
    # ===== Métodos para Dashboard =====
    
    def get_dashboard_summary(self):
        """Obtém dados resumidos para o dashboard de floricultura"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        result = {}
        
        # Total de flores em cultivo
        try:
            cursor.execute("SELECT SUM(quantity) as total FROM flower_cultivation WHERE status = 'Em Cultivo'")
            total_flowers = cursor.fetchone()
            result['total_flowers_in_cultivation'] = total_flowers['total'] if total_flowers['total'] else 0
        except Error as e:
            print(f"Erro ao obter total de flores em cultivo: {e}")
            result['total_flowers_in_cultivation'] = 0
        
        # Área total
        try:
            cursor.execute("SELECT SUM(area_m2) as total FROM flower_cultivation WHERE status = 'Em Cultivo'")
            total_area = cursor.fetchone()
            result['total_area_m2'] = total_area['total'] if total_area['total'] else 0
        except Error as e:
            print(f"Erro ao obter área total: {e}")
            result['total_area_m2'] = 0
        
        # Total de estufas
        try:
            cursor.execute("SELECT COUNT(*) as total FROM greenhouses")
            total_greenhouses = cursor.fetchone()
            result['total_greenhouses'] = total_greenhouses['total']
        except Error as e:
            print(f"Erro ao obter total de estufas: {e}")
            result['total_greenhouses'] = 0
        
        # Flores por espécie
        try:
            cursor.execute("""
                SELECT species, SUM(quantity) as quantity 
                FROM flower_cultivation 
                WHERE status = 'Em Cultivo' 
                GROUP BY species 
                ORDER BY quantity DESC
            """)
            result['flowers_by_species'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter flores por espécie: {e}")
            result['flowers_by_species'] = []
        
        # Colheitas por mês
        try:
            cursor.execute("""
                SELECT DATE_FORMAT(harvest_date, '%Y-%m') as month, SUM(quantity) as quantity 
                FROM flower_harvest_records 
                WHERE harvest_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) 
                GROUP BY month 
                ORDER BY month
            """)
            result['harvest_by_month'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter colheitas por mês: {e}")
            result['harvest_by_month'] = []
        
        # Vendas por mês
        try:
            cursor.execute("""
                SELECT DATE_FORMAT(sale_date, '%Y-%m') as month, SUM(total_value) as total_value 
                FROM flower_sale_records 
                WHERE sale_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) 
                GROUP BY month 
                ORDER BY month
            """)
            result['sales_by_month'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter vendas por mês: {e}")
            result['sales_by_month'] = []
        
        # Distribuição de qualidade
        try:
            cursor.execute("""
                SELECT quality_grade as grade, 
                       COUNT(*) * 100.0 / (SELECT COUNT(*) FROM flower_harvest_records) as percentage 
                FROM flower_harvest_records 
                GROUP BY quality_grade 
                ORDER BY quality_grade
            """)
            result['quality_distribution'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter distribuição de qualidade: {e}")
            result['quality_distribution'] = []
        
        cursor.close()
        return result
    
    def get_greenhouse_dashboard(self):
        """Obtém dados para o dashboard de estufas"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        result = {}
        
        # Estufas por tipo
        try:
            cursor.execute("SELECT type, COUNT(*) as count FROM greenhouses GROUP BY type")
            result['greenhouses_by_type'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter estufas por tipo: {e}")
            result['greenhouses_by_type'] = []
        
        # Tendências de temperatura
        try:
            cursor.execute("""
                SELECT record_date as date, 
                       MIN(temperature) as min, 
                       AVG(temperature) as avg, 
                       MAX(temperature) as max 
                FROM greenhouse_climate_records 
                WHERE record_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) 
                GROUP BY record_date 
                ORDER BY record_date
            """)
            result['temperature_trends'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter tendências de temperatura: {e}")
            result['temperature_trends'] = []
        
        # Tendências de umidade
        try:
            cursor.execute("""
                SELECT record_date as date, 
                       MIN(humidity) as min, 
                       AVG(humidity) as avg, 
                       MAX(humidity) as max 
                FROM greenhouse_climate_records 
                WHERE record_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) 
                GROUP BY record_date 
                ORDER BY record_date
            """)
            result['humidity_trends'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter tendências de umidade: {e}")
            result['humidity_trends'] = []
        
        # Taxa de ocupação
        try:
            cursor.execute("""
                SELECT g.id as greenhouse_id, 
                       g.name, 
                       g.area_m2 as capacity, 
                       COALESCE(SUM(f.area_m2), 0) as used,
                       COALESCE(SUM(f.area_m2) * 100 / g.area_m2, 0) as percentage
                FROM greenhouses g
                LEFT JOIN flower_cultivation f ON g.id = f.greenhouse_id AND f.status = 'Em Cultivo'
                GROUP BY g.id, g.name, g.area_m2
                ORDER BY percentage DESC
            """)
            result['occupancy_rate'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter taxa de ocupação: {e}")
            result['occupancy_rate'] = []
        
        cursor.close()
        return result
    
    def get_user_dashboard(self, user_id):
        """Obtém dados para o dashboard personalizado do usuário"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        result = {}
        
        # Informações do usuário
        try:
            cursor.execute("SELECT id, username, full_name FROM users WHERE id = %s", (user_id,))
            result['user_info'] = cursor.fetchone()
        except Error as e:
            print(f"Erro ao obter informações do usuário: {e}")
            result['user_info'] = {}
        
        # Atividades recentes
        try:
            cursor.execute("""
                SELECT id, activity_type, timestamp, details
                FROM user_floriculture_activities
                WHERE user_id = %s
                ORDER BY timestamp DESC
                LIMIT 5
            """, (user_id,))
            activities = cursor.fetchall()
            
            # Processar atividades para exibição
            recent_activities = []
            for activity in activities:
                if activity['details']:
                    details = json.loads(activity['details'])
                    summary = ""
                    
                    if activity['activity_type'] == 'cultivation' and details.get('action') == 'create':
                        summary = f"Criou cultivo de {details.get('quantity')} {details.get('species')}"
                    elif activity['activity_type'] == 'harvest' and details.get('action') == 'create':
                        summary = f"Registrou colheita de {details.get('quantity')} flores"
                    elif activity['activity_type'] == 'treatment' and details.get('action') == 'create':
                        summary = f"Aplicou {details.get('treatment_type')} com {details.get('product_used')}"
                    elif activity['activity_type'] == 'sale' and details.get('action') == 'create':
                        summary = f"Registrou venda de {details.get('quantity')} flores por R$ {details.get('total_value')}"
                    
                    if summary:
                        recent_activities.append({
                            'id': activity['id'],
                            'activity_type': activity['activity_type'],
                            'timestamp': activity['timestamp'],
                            'summary': summary
                        })
            
            result['recent_activities'] = recent_activities
        except Error as e:
            print(f"Erro ao obter atividades recentes: {e}")
            result['recent_activities'] = []
        
        # Próximas colheitas
        try:
            cursor.execute("""
                SELECT id, species, variety, expected_harvest_date, quantity,
                       DATEDIFF(expected_harvest_date, CURDATE()) as days_remaining
                FROM flower_cultivation
                WHERE user_id = %s
                  AND status = 'Em Cultivo'
                  AND expected_harvest_date IS NOT NULL
                  AND expected_harvest_date >= CURDATE()
                ORDER BY expected_harvest_date
                LIMIT 5
            """, (user_id,))
            result['upcoming_harvests'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter próximas colheitas: {e}")
            result['upcoming_harvests'] = []
        
        # Estatísticas de flores preferidas
        try:
            # Obter preferências do usuário
            preferences = self.get_user_preferences(user_id)
            preferred_flowers = []
            
            if preferences and preferences['preferred_flowers']:
                preferred_flowers = preferences['preferred_flowers']
                
                # Obter estatísticas para cada flor preferida
                stats = []
                for species in preferred_flowers:
                    # Total cultivado
                    cursor.execute("""
                        SELECT SUM(quantity) as total_cultivated
                        FROM flower_cultivation
                        WHERE user_id = %s AND species = %s
                    """, (user_id, species))
                    total_cultivated = cursor.fetchone()['total_cultivated'] or 0
                    
                    # Total colhido
                    cursor.execute("""
                        SELECT SUM(h.quantity) as total_harvested
                        FROM flower_harvest_records h
                        JOIN flower_cultivation f ON h.flower_id = f.id
                        WHERE f.user_id = %s AND f.species = %s
                    """, (user_id, species))
                    total_harvested = cursor.fetchone()['total_harvested'] or 0
                    
                    # Total vendido e receita
                    cursor.execute("""
                        SELECT SUM(s.quantity) as total_sales, SUM(s.total_value) as revenue
                        FROM flower_sale_records s
                        JOIN flower_cultivation f ON s.flower_id = f.id
                        WHERE f.user_id = %s AND f.species = %s
                    """, (user_id, species))
                    sales_data = cursor.fetchone()
                    total_sales = sales_data['total_sales'] or 0
                    revenue = sales_data['revenue'] or 0
                    
                    stats.append({
                        'species': species,
                        'total_cultivated': total_cultivated,
                        'total_harvested': total_harvested,
                        'total_sales': total_sales,
                        'revenue': revenue
                    })
                
                result['preferred_flowers_stats'] = stats
            else:
                result['preferred_flowers_stats'] = []
        except Error as e:
            print(f"Erro ao obter estatísticas de flores preferidas: {e}")
            result['preferred_flowers_stats'] = []
        
        # Contagem de notificações não lidas
        try:
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM user_floriculture_notifications
                WHERE user_id = %s AND is_read = 0
            """, (user_id,))
            result['unread_notifications_count'] = cursor.fetchone()['count']
        except Error as e:
            print(f"Erro ao obter contagem de notificações não lidas: {e}")
            result['unread_notifications_count'] = 0
        
        cursor.close()
        return result

# Instância global do banco de dados
floriculture_db = FloricultureDatabase()