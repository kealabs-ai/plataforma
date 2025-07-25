from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple
import os
import json
from dotenv import load_dotenv
from data.connection import connection_db as connection

# Carrega variáveis de ambiente
load_dotenv()

class LandscapingDatabase:
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
    
    # ===== Operações CRUD para Projetos de Paisagismo =====
    
    def create_project(self, user_id, name, client_name, project_type, area_m2, start_date, 
                      budget, expected_end_date=None, status="Em Andamento", address=None, description=None):
        """Cria um novo projeto de paisagismo"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO landscaping_projects 
        (user_id, name, client_name, project_type, area_m2, start_date, expected_end_date, budget, status, address, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (user_id, name, client_name, project_type, area_m2, start_date, 
                                  expected_end_date, budget, status, address, description))
            self.connection.commit()
            project_id = cursor.lastrowid
            return self.get_project(project_id)
        except Error as e:
            print(f"Erro ao criar projeto: {e}")
            return None
        finally:
            cursor.close()
    
    def get_project(self, project_id):
        """Obtém um projeto pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = "SELECT * FROM landscaping_projects WHERE id = %s"
        
        try:
            cursor.execute(query, (project_id,))
            project = cursor.fetchone()
            return project
        except Error as e:
            print(f"Erro ao obter projeto: {e}")
            return None
        finally:
            cursor.close()
    
    def get_all_projects(self, filters=None, page=1, page_size=10):
        """Obtém todos os projetos com filtros e paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = "SELECT * FROM landscaping_projects WHERE 1=1"
        params = []
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'project_type' in filters and filters['project_type']:
                query += " AND project_type = %s"
                params.append(filters['project_type'])
            
            if 'status' in filters and filters['status']:
                query += " AND status = %s"
                params.append(filters['status'])
            
            if 'client_name' in filters and filters['client_name']:
                query += " AND client_name LIKE %s"
                params.append(f"%{filters['client_name']}%")
            
            if 'user_id' in filters and filters['user_id']:
                query += " AND user_id = %s"
                params.append(filters['user_id'])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY start_date DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            projects = cursor.fetchall()
            return projects
        except Error as e:
            print(f"Erro ao obter projetos: {e}")
            return []
        finally:
            cursor.close()
    
    def count_projects(self, filters=None):
        """Conta o número total de projetos com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM landscaping_projects WHERE 1=1"
        params = []
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'project_type' in filters and filters['project_type']:
                query += " AND project_type = %s"
                params.append(filters['project_type'])
            
            if 'status' in filters and filters['status']:
                query += " AND status = %s"
                params.append(filters['status'])
            
            if 'client_name' in filters and filters['client_name']:
                query += " AND client_name LIKE %s"
                params.append(f"%{filters['client_name']}%")
            
            if 'user_id' in filters and filters['user_id']:
                query += " AND user_id = %s"
                params.append(filters['user_id'])
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar projetos: {e}")
            return 0
        finally:
            cursor.close()
    
    def update_project(self, project_id, user_id, update_data):
        """Atualiza um projeto"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o projeto existe e pertence ao usuário
        project = self.get_project(project_id)
        if not project or project['user_id'] != user_id:
            return None
        
        # Construir a consulta de atualização
        query = "UPDATE landscaping_projects SET "
        params = []
        
        # Adicionar campos a serem atualizados
        update_fields = []
        for key, value in update_data.items():
            if key in ['name', 'client_name', 'project_type', 'area_m2', 'start_date', 
                      'expected_end_date', 'budget', 'status', 'address', 'description']:
                update_fields.append(f"{key} = %s")
                params.append(value)
        
        if not update_fields:
            return project  # Nada para atualizar
        
        query += ", ".join(update_fields)
        query += ", updated_at = NOW() WHERE id = %s"
        params.append(project_id)
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return self.get_project(project_id)
        except Error as e:
            print(f"Erro ao atualizar projeto: {e}")
            return None
        finally:
            cursor.close()
    
    def delete_project(self, project_id, user_id):
        """Exclui um projeto"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o projeto existe e pertence ao usuário
        project = self.get_project(project_id)
        if not project or project['user_id'] != user_id:
            return False
        
        query = "DELETE FROM landscaping_projects WHERE id = %s"
        
        try:
            cursor.execute(query, (project_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao excluir projeto: {e}")
            return False
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Tarefas de Projetos =====
    
    def create_task(self, project_id, user_id, task_name, description, start_date, 
                   end_date=None, status="Pendente", assigned_to=None, priority="Média"):
        """Cria uma nova tarefa para um projeto"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o projeto existe e pertence ao usuário
        project = self.get_project(project_id)
        if not project or project['user_id'] != user_id:
            return None
        
        query = """
        INSERT INTO landscaping_tasks 
        (project_id, user_id, task_name, description, start_date, end_date, status, assigned_to, priority)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (project_id, user_id, task_name, description, start_date, 
                                  end_date, status, assigned_to, priority))
            self.connection.commit()
            task_id = cursor.lastrowid
            return self.get_task(task_id)
        except Error as e:
            print(f"Erro ao criar tarefa: {e}")
            return None
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Clientes CRM =====
    
    def create_client(self, user_id, client_name, contact_person=None, email=None, phone_number=None, 
                     address=None, city=None, state=None, zip_code=None, client_type=None, 
                     industry=None, status="Lead", last_interaction_date=None, next_follow_up_date=None, notes=None):
        """Cria um novo cliente CRM"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = """
        INSERT INTO landscaping_crm_clients 
        (user_id, client_name, contact_person, email, phone_number, address, city, state, zip_code, 
         client_type, industry, status, last_interaction_date, next_follow_up_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (user_id, client_name, contact_person, email, phone_number, address, 
                                  city, state, zip_code, client_type, industry, status, 
                                  last_interaction_date, next_follow_up_date, notes))
            self.connection.commit()
            client_id = cursor.lastrowid
            return self.get_client(client_id)
        except Error as e:
            print(f"Erro ao criar cliente: {e}")
            return None
        finally:
            cursor.close()
    
    def get_client(self, client_id):
        """Obtém um cliente pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = "SELECT * FROM landscaping_crm_clients WHERE id = %s"
        
        try:
            cursor.execute(query, (client_id,))
            client = cursor.fetchone()
            return client
        except Error as e:
            print(f"Erro ao obter cliente: {e}")
            return None
        finally:
            cursor.close()
    
    def get_all_clients(self, filters=None, page=1, page_size=10):
        """Obtém todos os clientes com filtros e paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = "SELECT * FROM landscaping_crm_clients WHERE 1=1"
        params = []
        
        if filters:
            if 'user_id' in filters and filters['user_id']:
                query += " AND user_id = %s"
                params.append(filters['user_id'])
            
            if 'status' in filters and filters['status']:
                query += " AND status = %s"
                params.append(filters['status'])
            
            if 'client_name' in filters and filters['client_name']:
                query += " AND client_name LIKE %s"
                params.append(f"%{filters['client_name']}%")
            
            if 'industry' in filters and filters['industry']:
                query += " AND industry = %s"
                params.append(filters['industry'])
        
        query += " ORDER BY client_name ASC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            clients = cursor.fetchall()
            return clients
        except Error as e:
            print(f"Erro ao obter clientes: {e}")
            return []
        finally:
            cursor.close()
    
    def count_clients(self, filters=None):
        """Conta o número total de clientes com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        query = "SELECT COUNT(*) FROM landscaping_crm_clients WHERE 1=1"
        params = []
        
        if filters:
            if 'user_id' in filters and filters['user_id']:
                query += " AND user_id = %s"
                params.append(filters['user_id'])
            
            if 'status' in filters and filters['status']:
                query += " AND status = %s"
                params.append(filters['status'])
            
            if 'client_name' in filters and filters['client_name']:
                query += " AND client_name LIKE %s"
                params.append(f"%{filters['client_name']}%")
            
            if 'industry' in filters and filters['industry']:
                query += " AND industry = %s"
                params.append(filters['industry'])
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar clientes: {e}")
            return 0
        finally:
            cursor.close()
    
    def update_client(self, client_id, user_id, update_data):
        """Atualiza um cliente"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o cliente existe e pertence ao usuário
        client = self.get_client(client_id)
        if not client or client['user_id'] != user_id:
            return None
        
        # Construir a consulta de atualização
        query = "UPDATE landscaping_crm_clients SET "
        params = []
        
        update_fields = []
        for key, value in update_data.items():
            if key in ['client_name', 'contact_person', 'email', 'phone_number', 'address', 
                      'city', 'state', 'zip_code', 'client_type', 'industry', 'status', 
                      'last_interaction_date', 'next_follow_up_date', 'notes']:
                update_fields.append(f"{key} = %s")
                params.append(value)
        
        if not update_fields:
            return client
        
        query += ", ".join(update_fields)
        query += ", updated_at = NOW() WHERE id = %s"
        params.append(client_id)
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return self.get_client(client_id)
        except Error as e:
            print(f"Erro ao atualizar cliente: {e}")
            return None
        finally:
            cursor.close()
    
    def delete_client(self, client_id, user_id):
        """Exclui um cliente"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o cliente existe e pertence ao usuário
        client = self.get_client(client_id)
        if not client or client['user_id'] != user_id:
            return False
        
        query = "DELETE FROM landscaping_crm_clients WHERE id = %s"
        
        try:
            cursor.execute(query, (client_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao excluir cliente: {e}")
            return False
        finally:
            cursor.close()
    
    def get_task(self, task_id):
        """Obtém uma tarefa pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT t.*, p.name as project_name
        FROM landscaping_tasks t
        JOIN landscaping_projects p ON t.project_id = p.id
        WHERE t.id = %s
        """
        
        try:
            cursor.execute(query, (task_id,))
            task = cursor.fetchone()
            return task
        except Error as e:
            print(f"Erro ao obter tarefa: {e}")
            return None
        finally:
            cursor.close()
    
    def get_project_tasks(self, project_id, filters=None, page=1, page_size=10):
        """Obtém tarefas de um projeto com filtros e paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = """
        SELECT t.*, p.name as project_name
        FROM landscaping_tasks t
        JOIN landscaping_projects p ON t.project_id = p.id
        WHERE t.project_id = %s
        """
        params = [project_id]
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'status' in filters and filters['status']:
                query += " AND t.status = %s"
                params.append(filters['status'])
            
            if 'priority' in filters and filters['priority']:
                query += " AND t.priority = %s"
                params.append(filters['priority'])
            
            if 'assigned_to' in filters and filters['assigned_to']:
                query += " AND t.assigned_to LIKE %s"
                params.append(f"%{filters['assigned_to']}%")
        
        # Adicionar ordenação e paginação
        query += " ORDER BY t.start_date ASC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            tasks = cursor.fetchall()
            return tasks
        except Error as e:
            print(f"Erro ao obter tarefas: {e}")
            return []
        finally:
            cursor.close()
    
    def count_project_tasks(self, project_id, filters=None):
        """Conta o número total de tarefas de um projeto com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM landscaping_tasks WHERE project_id = %s"
        params = [project_id]
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'status' in filters and filters['status']:
                query += " AND status = %s"
                params.append(filters['status'])
            
            if 'priority' in filters and filters['priority']:
                query += " AND priority = %s"
                params.append(filters['priority'])
            
            if 'assigned_to' in filters and filters['assigned_to']:
                query += " AND assigned_to LIKE %s"
                params.append(f"%{filters['assigned_to']}%")
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar tarefas: {e}")
            return 0
        finally:
            cursor.close()
    
    def update_task(self, task_id, user_id, update_data):
        """Atualiza uma tarefa"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se a tarefa existe
        task = self.get_task(task_id)
        if not task:
            return None
        
        # Verificar se o usuário tem permissão para atualizar a tarefa
        project = self.get_project(task['project_id'])
        if not project or project['user_id'] != user_id:
            return None
        
        # Construir a consulta de atualização
        query = "UPDATE landscaping_tasks SET "
        params = []
        
        # Adicionar campos a serem atualizados
        update_fields = []
        for key, value in update_data.items():
            if key in ['task_name', 'description', 'start_date', 'end_date', 'status', 'assigned_to', 'priority']:
                update_fields.append(f"{key} = %s")
                params.append(value)
        
        if not update_fields:
            return task  # Nada para atualizar
        
        query += ", ".join(update_fields)
        query += " WHERE id = %s"
        params.append(task_id)
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return self.get_task(task_id)
        except Error as e:
            print(f"Erro ao atualizar tarefa: {e}")
            return None
        finally:
            cursor.close()
    
    def delete_task(self, task_id, user_id):
        """Exclui uma tarefa"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se a tarefa existe
        task = self.get_task(task_id)
        if not task:
            return False
        
        # Verificar se o usuário tem permissão para excluir a tarefa
        project = self.get_project(task['project_id'])
        if not project or project['user_id'] != user_id:
            return False
        
        query = "DELETE FROM landscaping_tasks WHERE id = %s"
        
        try:
            cursor.execute(query, (task_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao excluir tarefa: {e}")
            return False
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Materiais de Projetos =====
    
    def create_material(self, project_id, user_id, name, category, quantity, unit, unit_price, 
                       supplier=None, purchase_date=None, notes=None):
        """Cria um novo material para um projeto"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o projeto existe e pertence ao usuário
        project = self.get_project(project_id)
        if not project or project['user_id'] != user_id:
            return None
        
        query = """
        INSERT INTO landscaping_materials 
        (project_id, user_id, name, category, quantity, unit, unit_price, supplier, purchase_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (project_id, user_id, name, category, quantity, unit, 
                                  unit_price, supplier, purchase_date, notes))
            self.connection.commit()
            material_id = cursor.lastrowid
            return self.get_material(material_id)
        except Error as e:
            print(f"Erro ao criar material: {e}")
            return None
        finally:
            cursor.close()
    
    def get_material(self, material_id):
        """Obtém um material pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT m.*, p.name as project_name, m.quantity * m.unit_price as total_price
        FROM landscaping_materials m
        JOIN landscaping_projects p ON m.project_id = p.id
        WHERE m.id = %s
        """
        
        try:
            cursor.execute(query, (material_id,))
            material = cursor.fetchone()
            return material
        except Error as e:
            print(f"Erro ao obter material: {e}")
            return None
        finally:
            cursor.close()
    
    def get_project_materials(self, project_id, filters=None, page=1, page_size=10):
        """Obtém materiais de um projeto com filtros e paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = """
        SELECT m.*, p.name as project_name, m.quantity * m.unit_price as total_price
        FROM landscaping_materials m
        JOIN landscaping_projects p ON m.project_id = p.id
        WHERE m.project_id = %s
        """
        params = [project_id]
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'category' in filters and filters['category']:
                query += " AND m.category = %s"
                params.append(filters['category'])
            
            if 'supplier' in filters and filters['supplier']:
                query += " AND m.supplier LIKE %s"
                params.append(f"%{filters['supplier']}%")
            
            if 'start_date' in filters and filters['start_date']:
                query += " AND m.purchase_date >= %s"
                params.append(filters['start_date'])
            
            if 'end_date' in filters and filters['end_date']:
                query += " AND m.purchase_date <= %s"
                params.append(filters['end_date'])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY m.purchase_date DESC, m.name ASC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            materials = cursor.fetchall()
            return materials
        except Error as e:
            print(f"Erro ao obter materiais: {e}")
            return []
        finally:
            cursor.close()
    
    def count_project_materials(self, project_id, filters=None):
        """Conta o número total de materiais de um projeto com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM landscaping_materials WHERE project_id = %s"
        params = [project_id]
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'category' in filters and filters['category']:
                query += " AND category = %s"
                params.append(filters['category'])
            
            if 'supplier' in filters and filters['supplier']:
                query += " AND supplier LIKE %s"
                params.append(f"%{filters['supplier']}%")
            
            if 'start_date' in filters and filters['start_date']:
                query += " AND purchase_date >= %s"
                params.append(filters['start_date'])
            
            if 'end_date' in filters and filters['end_date']:
                query += " AND purchase_date <= %s"
                params.append(filters['end_date'])
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar materiais: {e}")
            return 0
        finally:
            cursor.close()
    
    def update_material(self, material_id, user_id, update_data):
        """Atualiza um material"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o material existe
        material = self.get_material(material_id)
        if not material:
            return None
        
        # Verificar se o usuário tem permissão para atualizar o material
        project = self.get_project(material['project_id'])
        if not project or project['user_id'] != user_id:
            return None
        
        # Construir a consulta de atualização
        query = "UPDATE landscaping_materials SET "
        params = []
        
        # Adicionar campos a serem atualizados
        update_fields = []
        for key, value in update_data.items():
            if key in ['name', 'category', 'quantity', 'unit', 'unit_price', 'supplier', 'purchase_date', 'notes']:
                update_fields.append(f"{key} = %s")
                params.append(value)
        
        if not update_fields:
            return material  # Nada para atualizar
        
        query += ", ".join(update_fields)
        query += " WHERE id = %s"
        params.append(material_id)
        
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return self.get_material(material_id)
        except Error as e:
            print(f"Erro ao atualizar material: {e}")
            return None
        finally:
            cursor.close()
    
    def delete_material(self, material_id, user_id):
        """Exclui um material"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o material existe
        material = self.get_material(material_id)
        if not material:
            return False
        
        # Verificar se o usuário tem permissão para excluir o material
        project = self.get_project(material['project_id'])
        if not project or project['user_id'] != user_id:
            return False
        
        query = "DELETE FROM landscaping_materials WHERE id = %s"
        
        try:
            cursor.execute(query, (material_id,))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao excluir material: {e}")
            return False
        finally:
            cursor.close()
    
    # ===== Operações CRUD para Registros de Plantio =====
    
    def create_planting_record(self, project_id, user_id, planting_date, plant_type, 
                              species, quantity, area_m2, notes=None):
        """Cria um novo registro de plantio para um projeto"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Verificar se o projeto existe e pertence ao usuário
        project = self.get_project(project_id)
        if not project or project['user_id'] != user_id:
            return None
        
        query = """
        INSERT INTO landscaping_planting_records 
        (project_id, user_id, planting_date, plant_type, species, quantity, area_m2, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            cursor.execute(query, (project_id, user_id, planting_date, plant_type, 
                                  species, quantity, area_m2, notes))
            self.connection.commit()
            record_id = cursor.lastrowid
            return self.get_planting_record(record_id)
        except Error as e:
            print(f"Erro ao criar registro de plantio: {e}")
            return None
        finally:
            cursor.close()
    
    def get_planting_record(self, record_id):
        """Obtém um registro de plantio pelo ID"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT r.*, p.name as project_name
        FROM landscaping_planting_records r
        JOIN landscaping_projects p ON r.project_id = p.id
        WHERE r.id = %s
        """
        
        try:
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
            return record
        except Error as e:
            print(f"Erro ao obter registro de plantio: {e}")
            return None
        finally:
            cursor.close()
    
    def get_project_planting_records(self, project_id, filters=None, page=1, page_size=10):
        """Obtém registros de plantio de um projeto com filtros e paginação"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Construir a consulta base
        query = """
        SELECT r.*, p.name as project_name
        FROM landscaping_planting_records r
        JOIN landscaping_projects p ON r.project_id = p.id
        WHERE r.project_id = %s
        """
        params = [project_id]
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'plant_type' in filters and filters['plant_type']:
                query += " AND r.plant_type = %s"
                params.append(filters['plant_type'])
            
            if 'species' in filters and filters['species']:
                query += " AND r.species LIKE %s"
                params.append(f"%{filters['species']}%")
            
            if 'start_date' in filters and filters['start_date']:
                query += " AND r.planting_date >= %s"
                params.append(filters['start_date'])
            
            if 'end_date' in filters and filters['end_date']:
                query += " AND r.planting_date <= %s"
                params.append(filters['end_date'])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY r.planting_date DESC"
        query += " LIMIT %s OFFSET %s"
        
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        try:
            cursor.execute(query, params)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Erro ao obter registros de plantio: {e}")
            return []
        finally:
            cursor.close()
    
    def count_project_planting_records(self, project_id, filters=None):
        """Conta o número total de registros de plantio de um projeto com filtros"""
        self.ensure_connection()
        cursor = self.connection.cursor()
        
        # Construir a consulta base
        query = "SELECT COUNT(*) FROM landscaping_planting_records WHERE project_id = %s"
        params = [project_id]
        
        # Adicionar filtros se fornecidos
        if filters:
            if 'plant_type' in filters and filters['plant_type']:
                query += " AND plant_type = %s"
                params.append(filters['plant_type'])
            
            if 'species' in filters and filters['species']:
                query += " AND species LIKE %s"
                params.append(f"%{filters['species']}%")
            
            if 'start_date' in filters and filters['start_date']:
                query += " AND planting_date >= %s"
                params.append(filters['start_date'])
            
            if 'end_date' in filters and filters['end_date']:
                query += " AND planting_date <= %s"
                params.append(filters['end_date'])
        
        try:
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        except Error as e:
            print(f"Erro ao contar registros de plantio: {e}")
            return 0
        finally:
            cursor.close()
    
    # ===== Métodos para Dashboard =====
    
    def get_dashboard_summary(self):
        """Obtém dados resumidos para o dashboard de paisagismo"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        result = {}
        
        # Total de projetos e por status
        try:
            cursor.execute("SELECT COUNT(*) as total FROM landscaping_projects")
            result['total_projects'] = cursor.fetchone()['total']
            
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM landscaping_projects 
                GROUP BY status 
                ORDER BY count DESC
            """)
            result['projects_by_status'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter total de projetos: {e}")
            result['total_projects'] = 0
            result['projects_by_status'] = []
        
        # Projetos por tipo
        try:
            cursor.execute("""
                SELECT project_type as type, COUNT(*) as count 
                FROM landscaping_projects 
                GROUP BY project_type 
                ORDER BY count DESC
            """)
            result['projects_by_type'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter projetos por tipo: {e}")
            result['projects_by_type'] = []
        
        # Área total e orçamento total
        try:
            cursor.execute("SELECT SUM(area_m2) as total_area FROM landscaping_projects")
            result['total_area_m2'] = cursor.fetchone()['total_area'] or 0
            
            cursor.execute("SELECT SUM(budget) as total_budget FROM landscaping_projects")
            result['total_budget'] = cursor.fetchone()['total_budget'] or 0
        except Error as e:
            print(f"Erro ao obter área e orçamento total: {e}")
            result['total_area_m2'] = 0
            result['total_budget'] = 0
        
        # Tarefas por status
        try:
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM landscaping_tasks 
                GROUP BY status 
                ORDER BY count DESC
            """)
            result['tasks_by_status'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter tarefas por status: {e}")
            result['tasks_by_status'] = []
        
        # Despesas por categoria
        try:
            cursor.execute("""
                SELECT category, SUM(amount) as total 
                FROM landscaping_expense_records 
                GROUP BY category 
                ORDER BY total DESC
            """)
            result['expenses_by_category'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter despesas por categoria: {e}")
            result['expenses_by_category'] = []
        
        # Plantio por tipo
        try:
            cursor.execute("""
                SELECT plant_type as type, SUM(quantity) as quantity 
                FROM landscaping_planting_records 
                GROUP BY plant_type 
                ORDER BY quantity DESC
            """)
            result['planting_by_type'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter plantio por tipo: {e}")
            result['planting_by_type'] = []
        
        # Horas de manutenção por mês
        try:
            cursor.execute("""
                SELECT DATE_FORMAT(maintenance_date, '%Y-%m') as month, SUM(hours_spent) as hours 
                FROM landscaping_maintenance_records 
                WHERE maintenance_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) 
                GROUP BY month 
                ORDER BY month
            """)
            result['maintenance_hours_by_month'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter horas de manutenção por mês: {e}")
            result['maintenance_hours_by_month'] = []
        
        cursor.close()
        return result
    
    def get_project_summary(self, project_id):
        """Obtém um resumo detalhado de um projeto específico"""
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        result = {}
        
        # Informações básicas do projeto
        try:
            project = self.get_project(project_id)
            if not project:
                return None
            
            result['project_info'] = project
        except Error as e:
            print(f"Erro ao obter informações do projeto: {e}")
            return None
        
        # Progresso de tarefas
        try:
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM landscaping_tasks 
                WHERE project_id = %s 
                GROUP BY status
            """, (project_id,))
            task_status = cursor.fetchall()
            
            # Calcular percentual de conclusão
            total_tasks = sum(item['count'] for item in task_status)
            completed_tasks = next((item['count'] for item in task_status if item['status'] == 'Concluída'), 0)
            
            result['task_status'] = task_status
            result['completion_percentage'] = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        except Error as e:
            print(f"Erro ao obter progresso de tarefas: {e}")
            result['task_status'] = []
            result['completion_percentage'] = 0
        
        # Total de despesas
        try:
            cursor.execute("""
                SELECT SUM(amount) as total_expenses 
                FROM landscaping_expense_records 
                WHERE project_id = %s
            """, (project_id,))
            expenses = cursor.fetchone()
            
            result['total_expenses'] = expenses['total_expenses'] or 0
            result['budget_percentage'] = (result['total_expenses'] / project['budget'] * 100) if project['budget'] > 0 else 0
        except Error as e:
            print(f"Erro ao obter total de despesas: {e}")
            result['total_expenses'] = 0
            result['budget_percentage'] = 0
        
        # Resumo de plantio
        try:
            cursor.execute("""
                SELECT plant_type, SUM(quantity) as quantity, SUM(area_m2) as area 
                FROM landscaping_planting_records 
                WHERE project_id = %s 
                GROUP BY plant_type
            """, (project_id,))
            result['planting_summary'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter resumo de plantio: {e}")
            result['planting_summary'] = []
        
        # Próximas tarefas
        try:
            cursor.execute("""
                SELECT id, task_name, start_date, priority, assigned_to 
                FROM landscaping_tasks 
                WHERE project_id = %s AND status != 'Concluída' 
                ORDER BY start_date ASC 
                LIMIT 5
            """, (project_id,))
            result['upcoming_tasks'] = cursor.fetchall()
        except Error as e:
            print(f"Erro ao obter próximas tarefas: {e}")
            result['upcoming_tasks'] = []
        
        cursor.close()
        return result

# Instância global do banco de dados
landscaping_db = LandscapingDatabase()