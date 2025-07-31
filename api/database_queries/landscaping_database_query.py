"""
Módulo de acesso ao banco de dados para o sistema de paisagismo.
Implementa as operações CRUD para projetos, fornecedores, serviços, orçamentos e manutenção de paisagismo.
"""

from typing import Dict, List, Optional, Any
from data.connection import *
from datetime import date, datetime
import json

# Operações para Projetos de Paisagismo
def create_project(
    user_id: int,
    name: str,
    client_name: str,
    area_m2: float,
    location: str,
    start_date: str,
    end_date: Optional[str] = None,
    budget: Optional[float] = None,
    status: str = "planejamento",
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um novo projeto de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO landscaping_projects (
            user_id, name, client_name, area_m2, location, 
            start_date, end_date, budget, status, description
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        cursor.execute(query, (
            user_id, name, client_name, area_m2, location,
            start_date, end_date, budget, status, description
        ))
        
        project_id = cursor.lastrowid
        conn.commit()
        
        # Buscar o registro recém-criado
        return get_project(project_id)
    except Exception as e:
        print(f"Erro ao criar projeto de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_projects(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todos os projetos de paisagismo com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = "SELECT * FROM landscaping_projects WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "client_name" in filters:
            query += " AND client_name LIKE %s"
            params.append(f"%{filters['client_name']}%")
        
        # Adicionar ordenação e paginação
        query += " ORDER BY start_date DESC LIMIT %s OFFSET %s"
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter projetos de paisagismo: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_projects(filters: Dict[str, Any]) -> int:
    """
    Conta o total de projetos de paisagismo com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM landscaping_projects WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "client_name" in filters:
            query += " AND client_name LIKE %s"
            params.append(f"%{filters['client_name']}%")
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar projetos de paisagismo: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_project(project_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um projeto específico de paisagismo pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM landscaping_projects WHERE id = %s"
        cursor.execute(query, (project_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter projeto de paisagismo: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_project(
    project_id: int,
    user_id: int,
    update_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Atualiza um projeto de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o projeto existe e pertence ao usuário
        check_query = "SELECT id FROM landscaping_projects WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (project_id, user_id))
        if not cursor.fetchone():
            return None
        
        # Construir a consulta de atualização
        if not update_data:
            return get_project(project_id)
        
        query = "UPDATE landscaping_projects SET "
        params = []
        
        for key, value in update_data.items():
            query += f"{key} = %s, "
            params.append(value)
        
        # Remover a vírgula final e adicionar a condição WHERE
        query = query[:-2] + " WHERE id = %s AND user_id = %s"
        params.extend([project_id, user_id])
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            return get_project(project_id)
        return None
    except Exception as e:
        print(f"Erro ao atualizar projeto de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def update_project_status_data(
    project_id: int,
    user_id: int,
    new_status: str
) -> Optional[Dict[str, Any]]:
    """
    Atualiza apenas o status de um projeto de paisagismo.
    Função otimizada para atualizações rápidas de status no quadro Kanban.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o projeto existe e pertence ao usuário
        check_query = "SELECT id, status FROM landscaping_projects WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (project_id, user_id))
        project = cursor.fetchone()
        if not project:
            return None
        
        # Registrar a mudança de status
        old_status = project[1] if len(project) > 1 else "desconhecido"
        
        # Atualizar apenas o status
        query = "UPDATE landscaping_projects SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s AND user_id = %s"
        cursor.execute(query, (new_status, project_id, user_id))
        conn.commit()
        
        if cursor.rowcount > 0:
            # Retornar um objeto simplificado com as informações essenciais
            return {
                "id": project_id,
                "status": new_status,
                "previous_status": old_status,
                "updated": True,
                "timestamp": datetime.now().isoformat()
            }
        return None
    except Exception as e:
        print(f"Erro ao atualizar status do projeto: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def delete_project(project_id: int, user_id: int) -> bool:
    """
    Remove um projeto de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM landscaping_projects WHERE id = %s AND user_id = %s"
        cursor.execute(query, (project_id, user_id))
        conn.commit()
        
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover projeto de paisagismo: {str(e)}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# Operações para Fornecedores de Paisagismo
def create_supplier(
    user_id: int,
    name: str,
    contact_person: str,
    phone: str,
    email: str,
    products: str,
    last_contract: Optional[str] = None,
    status: str = "Ativo",
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um novo fornecedor de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO landscaping_suppliers (
            user_id, name, contact_person, phone, email, 
            products, last_contract, status, notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        cursor.execute(query, (
            user_id, name, contact_person, phone, email,
            products, last_contract, status, notes
        ))
        
        supplier_id = cursor.lastrowid
        conn.commit()
        
        # Buscar o registro recém-criado
        return get_supplier(supplier_id)
    except Exception as e:
        print(f"Erro ao criar fornecedor de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_suppliers(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todos os fornecedores de paisagismo com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = "SELECT * FROM landscaping_suppliers WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "name" in filters:
            query += " AND name LIKE %s"
            params.append(f"%{filters['name']}%")
        
        # Adicionar ordenação e paginação
        query += " ORDER BY name LIMIT %s OFFSET %s"
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter fornecedores de paisagismo: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_suppliers(filters: Dict[str, Any]) -> int:
    """
    Conta o total de fornecedores de paisagismo com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM landscaping_suppliers WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "name" in filters:
            query += " AND name LIKE %s"
            params.append(f"%{filters['name']}%")
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar fornecedores de paisagismo: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def update_quote(quote_id: int, user_id: int, quote_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Atualiza um orçamento de paisagismo e seus itens.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar se o orçamento existe
        check_query = "SELECT id FROM landscaping_quotes WHERE id = %s"
        cursor.execute(check_query, (quote_id,))
        if not cursor.fetchone():
            return None
        
        # Atualizar dados básicos do orçamento
        update_fields = []
        update_values = []
        
        # Campos que podem ser atualizados
        updatable_fields = [
            "client_id", "description", "valid_until", 
            "total_value", "notes", "status"
        ]
        
        for field in updatable_fields:
            if field in quote_data and quote_data[field] is not None:
                update_fields.append(f"{field} = %s")
                update_values.append(quote_data[field])
        
        if update_fields:
            # Adicionar updated_at
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            
            # Construir e executar a consulta de atualização
            update_query = f"UPDATE landscaping_quotes SET {', '.join(update_fields)} WHERE id = %s"
            update_values.append(quote_id)
            cursor.execute(update_query, update_values)
        
        # Atualizar itens do orçamento, se fornecidos
        if "items" in quote_data and quote_data["items"]:
            # Remover itens existentes
            cursor.execute("DELETE FROM landscaping_quote_items WHERE quote_id = %s", (quote_id,))
            
            # Inserir novos itens
            for item in quote_data["items"]:
                subtotal = item["quantity"] * item["unit_price"]
                insert_item_query = """
                INSERT INTO landscaping_quote_items 
                (quote_id, service_id, quantity, unit_price, subtotal, description) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                cursor.execute(
                    insert_item_query, 
                    (
                        quote_id, 
                        item["service_id"], 
                        item["quantity"], 
                        item["unit_price"], 
                        subtotal,
                        item.get("description", "")
                    )
                )
        
        # Confirmar transação
        conn.commit()
        
        # Retornar o orçamento atualizado
        return get_quote(quote_id)
    except Exception as e:
        # Reverter transação em caso de erro
        conn.rollback()
        print(f"Erro ao atualizar orçamento: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_supplier(supplier_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um fornecedor específico pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM landscaping_suppliers WHERE id = %s"
        cursor.execute(query, (supplier_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter fornecedor de paisagismo: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_supplier(
    supplier_id: int,
    user_id: int,
    update_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Atualiza um fornecedor de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o fornecedor existe e pertence ao usuário
        check_query = "SELECT id FROM landscaping_suppliers WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (supplier_id, user_id))
        if not cursor.fetchone():
            return None
        
        # Construir a consulta de atualização
        if not update_data:
            return get_supplier(supplier_id)
        
        query = "UPDATE landscaping_suppliers SET "
        params = []
        
        for key, value in update_data.items():
            query += f"{key} = %s, "
            params.append(value)
        
        # Remover a vírgula final e adicionar a condição WHERE
        query = query[:-2] + " WHERE id = %s AND user_id = %s"
        params.extend([supplier_id, user_id])
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            return get_supplier(supplier_id)
        return None
    except Exception as e:
        print(f"Erro ao atualizar fornecedor de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def delete_supplier(supplier_id: int, user_id: int) -> bool:
    """
    Remove um fornecedor de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM landscaping_suppliers WHERE id = %s AND user_id = %s"
        cursor.execute(query, (supplier_id, user_id))
        conn.commit()
        
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover fornecedor de paisagismo: {str(e)}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# Operações para Serviços de Paisagismo
def create_service(
    user_id: int,
    service_name: str,
    category: str,
    description: str,
    average_duration: float,
    base_price: float,
    status: str = "Ativo"
) -> Dict[str, Any]:
    """
    Cria um novo serviço de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO landscaping_services (
            user_id, service_name, category, description, 
            average_duration, base_price, status
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        cursor.execute(query, (
            user_id, service_name, category, description,
            average_duration, base_price, status
        ))
        
        service_id = cursor.lastrowid
        conn.commit()
        
        # Buscar o registro recém-criado
        return get_service(service_id)
    except Exception as e:
        print(f"Erro ao criar serviço de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_services(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todos os serviços de paisagismo com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = "SELECT * FROM landscaping_services WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "category" in filters:
            query += " AND category = %s"
            params.append(filters["category"])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY service_name LIMIT %s OFFSET %s"
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter serviços de paisagismo: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_services(filters: Dict[str, Any]) -> int:
    """
    Conta o total de serviços de paisagismo com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM landscaping_services WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "category" in filters:
            query += " AND category = %s"
            params.append(filters["category"])
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar serviços de paisagismo: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_service(service_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um serviço específico pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM landscaping_services WHERE id = %s"
        cursor.execute(query, (service_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter serviço de paisagismo: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_service(
    service_id: int,
    user_id: int,
    update_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Atualiza um serviço de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o serviço existe e pertence ao usuário
        check_query = "SELECT id FROM landscaping_services WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (service_id, user_id))
        if not cursor.fetchone():
            return None
        
        # Construir a consulta de atualização
        if not update_data:
            return get_service(service_id)
        
        query = "UPDATE landscaping_services SET "
        params = []
        
        for key, value in update_data.items():
            query += f"{key} = %s, "
            params.append(value)
        
        # Remover a vírgula final e adicionar a condição WHERE
        query = query[:-2] + " WHERE id = %s AND user_id = %s"
        params.extend([service_id, user_id])
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            return get_service(service_id)
        return None
    except Exception as e:
        print(f"Erro ao atualizar serviço de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

# Operações para Orçamentos de Paisagismo
def create_quote(
    user_id: int,
    client_id: int,
    description: str,
    created_at: str,
    valid_until: str,
    total_value: float,
    notes: Optional[str] = None,
    status: str = "Pendente",
    items: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Cria um novo orçamento de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Inserir o orçamento
        query = """
        INSERT INTO landscaping_quotes (
            user_id, client_id, description, created_at, 
            valid_until, total_value, notes, status
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        cursor.execute(query, (
            user_id, client_id, description, created_at,
            valid_until, total_value, notes, status
        ))
        
        quote_id = cursor.lastrowid
        
        # Inserir os itens do orçamento
        if items:
            for item in items:
                item_query = """
                INSERT INTO landscaping_quote_items (
                    quote_id, service_id, quantity, unit_price, subtotal, description
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
                """
                
                cursor.execute(item_query, (
                    quote_id, item["service_id"], item["quantity"],
                    item["unit_price"], item["subtotal"], item.get("description", "")
                ))
        
        conn.commit()
        
        # Buscar o registro recém-criado
        result = get_quote(quote_id)
        
        # Convert datetime objects to strings
        if result:
            if "created_at" in result and isinstance(result["created_at"], datetime):
                result["created_at"] = result["created_at"].isoformat()
            if "valid_until" in result and isinstance(result["valid_until"], date):
                result["valid_until"] = result["valid_until"].isoformat()
            if "updated_at" in result and isinstance(result["updated_at"], datetime):
                result["updated_at"] = result["updated_at"].isoformat()
        
        return result
    except Exception as e:
        print(f"Erro ao criar orçamento de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_quotes(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todos os orçamentos de paisagismo com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = "SELECT * FROM landscaping_quotes WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "client" in filters:
            query += " AND client_id = %s"
            params.append(filters["client"])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        quotes = cursor.fetchall()
        
        # Buscar os itens de cada orçamento e converter datas para string
        for quote in quotes:
            # Add items to the quote
            quote["items"] = get_quote_items(quote["id"])
            
            # Convert datetime objects to strings
            if "created_at" in quote and isinstance(quote["created_at"], datetime):
                quote["created_at"] = quote["created_at"].isoformat()
            if "valid_until" in quote and isinstance(quote["valid_until"], date):
                quote["valid_until"] = quote["valid_until"].isoformat()
            if "updated_at" in quote and isinstance(quote["updated_at"], datetime):
                quote["updated_at"] = quote["updated_at"].isoformat()
        
        return quotes
    except Exception as e:
        print(f"Erro ao obter orçamentos de paisagismo: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_quotes(filters: Dict[str, Any]) -> int:
    """
    Conta o total de orçamentos de paisagismo com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM landscaping_quotes WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "client" in filters:
            query += " AND client_id = %s"
            params.append(filters["client"])
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar orçamentos de paisagismo: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_quote(quote_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um orçamento específico pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM landscaping_quotes WHERE id = %s"
        cursor.execute(query, (quote_id,))
        quote = cursor.fetchone()
        
        if quote:
            # Add items to the quote
            quote["items"] = get_quote_items(quote_id)
            
            # Convert datetime objects to strings
            if "created_at" in quote and isinstance(quote["created_at"], datetime):
                quote["created_at"] = quote["created_at"].isoformat()
            if "valid_until" in quote and isinstance(quote["valid_until"], date):
                quote["valid_until"] = quote["valid_until"].isoformat()
            if "updated_at" in quote and isinstance(quote["updated_at"], datetime):
                quote["updated_at"] = quote["updated_at"].isoformat()
        
        return quote
    except Exception as e:
        print(f"Erro ao obter orçamento de paisagismo: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_quote_items(quote_id: int) -> List[Dict[str, Any]]:
    """
    Obtém os itens de um orçamento específico.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT qi.*, s.service_name, s.category
        FROM landscaping_quote_items qi
        JOIN landscaping_services s ON qi.service_id = s.id
        WHERE qi.quote_id = %s
        """
        cursor.execute(query, (quote_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter itens de orçamento: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

# Operações para Manutenção de Paisagismo
def create_maintenance(
    user_id: int,
    project_id: int,
    date: str,
    type: str,
    description: str,
    cost: Optional[float] = None,
    duration_hours: Optional[float] = None,
    status: str = "concluído",
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um novo registro de manutenção de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar se o projeto existe e pertence ao usuário
        check_query = "SELECT id FROM landscaping_projects WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (project_id, user_id))
        if not cursor.fetchone():
            return None
        
        query = """
        INSERT INTO landscaping_maintenance_records (
            user_id, project_id, maintenance_date, maintenance_type, description, 
            cost, hours_spent, status, notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        cursor.execute(query, (
            user_id, project_id, date, type, description,
            cost, duration_hours, status, notes
        ))
        
        maintenance_id = cursor.lastrowid
        conn.commit()
        
        # Buscar o registro recém-criado
        return get_maintenance(maintenance_id)
    except Exception as e:
        print(f"Erro ao criar manutenção de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_maintenance(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todos os registros de manutenção com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = """
        SELECT m.*, p.name as project_name 
        FROM landscaping_maintenance_records m
        JOIN landscaping_projects p ON m.project_id = p.id
        WHERE 1=1
        """
        params = []
        
        if "user_id" in filters:
            query += " AND m.user_id = %s"
            params.append(filters["user_id"])
        
        if "project_id" in filters:
            query += " AND m.project_id = %s"
            params.append(filters["project_id"])
        
        if "type" in filters:
            query += " AND m.type = %s"
            params.append(filters["type"])
        
        if "status" in filters:
            query += " AND m.status = %s"
            params.append(filters["status"])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY m.maintenance_date DESC LIMIT %s OFFSET %s"
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter registros de manutenção: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_maintenance(filters: Dict[str, Any]) -> int:
    """
    Conta o total de registros de manutenção com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM landscaping_maintenance_records WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "project_id" in filters:
            query += " AND project_id = %s"
            params.append(filters["project_id"])
        
        if "type" in filters:
            query += " AND type = %s"
            params.append(filters["type"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar registros de manutenção: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_maintenance(maintenance_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um registro específico de manutenção pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT m.*, p.name as project_name 
        FROM landscaping_maintenance_records m
        JOIN landscaping_projects p ON m.project_id = p.id
        WHERE m.id = %s
        """
        cursor.execute(query, (maintenance_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter registro de manutenção: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_maintenance(
    maintenance_id: int,
    user_id: int,
    update_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Atualiza um registro de manutenção.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o registro existe e pertence ao usuário
        check_query = "SELECT id FROM landscaping_maintenance_records WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (maintenance_id, user_id))
        if not cursor.fetchone():
            return None
        
        # Construir a consulta de atualização
        if not update_data:
            return get_maintenance(maintenance_id)
        
        query = "UPDATE landscaping_maintenance_records SET "
        params = []
        
        for key, value in update_data.items():
            # Mapear campos do modelo para os campos do banco de dados
            db_key = key
            if key == "date":
                db_key = "maintenance_date"
            elif key == "type":
                db_key = "maintenance_type"
            elif key == "duration_hours":
                db_key = "hours_spent"
                
            query += f"{db_key} = %s, "
            params.append(value)
        
        # Remover a vírgula final e adicionar a condição WHERE
        query = query[:-2] + " WHERE id = %s AND user_id = %s"
        params.extend([maintenance_id, user_id])
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            return get_maintenance(maintenance_id)
        return None
    except Exception as e:
        print(f"Erro ao atualizar registro de manutenção: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

# Operações para Dashboard de Paisagismo
def get_dashboard_summary(user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Obtém dados resumidos para o dashboard de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Filtro de usuário
        user_filter = ""
        params = []
        if user_id:
            user_filter = "WHERE user_id = %s"
            params.append(user_id)
        
        # 1. Resumo de projetos
        query_projects = f"""
        SELECT 
            COUNT(*) as total_projects,
            SUM(CASE WHEN status = 'Em Andamento' THEN 1 ELSE 0 END) as active_projects,
            SUM(CASE WHEN status = 'Concluído' THEN 1 ELSE 0 END) as completed_projects,
            SUM(CASE WHEN status = 'Cancelado' THEN 1 ELSE 0 END) as cancelled_projects
        FROM landscaping_projects
        {user_filter}
        """
        cursor.execute(query_projects, params)
        projects_summary = cursor.fetchone() or {
            "total_projects": 0,
            "active_projects": 0,
            "completed_projects": 0,
            "cancelled_projects": 0
        }
        
        # 2. Resumo de orçamento
        query_budget = f"""
        SELECT 
            SUM(budget) as total_budget,
            SUM(CASE WHEN status = 'concluído' THEN budget ELSE 0 END) as total_spent
        FROM landscaping_projects
        {user_filter}
        """
        cursor.execute(query_budget, params)
        budget_data = cursor.fetchone() or {"total_budget": 0, "total_spent": 0}
        
        total_budget = float(budget_data["total_budget"] or 0)
        total_spent = float(budget_data["total_spent"] or 0)
        percentage = 0
        if total_budget > 0:
            percentage = (total_spent / total_budget) * 100
        
        budget_summary = {
            "total_budget": total_budget,
            "total_spent": total_spent,
            "percentage": percentage
        }
        
        # 3. Projetos por tipo
        query_by_type = f"""
        SELECT 
            project_type as type,
            COUNT(*) as count
        FROM landscaping_projects
        {user_filter}
        GROUP BY project_type
        """
        cursor.execute(query_by_type, params)
        projects_by_type = cursor.fetchall() or []
        
        # 4. Tarefas por status (da tabela de manutenção)
        query_tasks = f"""
        SELECT 
            status,
            COUNT(*) as count
        FROM landscaping_maintenance_records
        {user_filter}
        GROUP BY status
        """
        cursor.execute(query_tasks, params)
        tasks_by_status = cursor.fetchall() or []
        
        # 5. Materiais por categoria (simulado)
        materials_by_category = [
            {"category": "Plantas", "total": 45000.0},
            {"category": "Materiais de Construção", "total": 65000.0},
            {"category": "Ferramentas", "total": 12000.0},
            {"category": "Outros", "total": 8000.0}
        ]
        
        # 6. Progresso mensal (simulado)
        monthly_progress = [
            {"month": "2024-01", "completed_tasks": 12},
            {"month": "2024-02", "completed_tasks": 18},
            {"month": "2024-03", "completed_tasks": 15},
            {"month": "2024-04", "completed_tasks": 20}
        ]
        
        # 7. Quantidade de clientes
        query_clients = f"""
        SELECT COUNT(*) as quantity_clients
        FROM landscaping_crm_clients
        {user_filter}
        """
        cursor.execute(query_clients, params)
        clients_data = cursor.fetchone() or {"quantity_clients": 0}
        quantity_clients = clients_data["quantity_clients"]
        
        return {
            "projects_summary": projects_summary,
            "budget_summary": budget_summary,
            "projects_by_type": projects_by_type,
            "tasks_by_status": tasks_by_status,
            "materials_by_category": materials_by_category,
            "monthly_progress": monthly_progress,
            "quantity_clients": quantity_clients
        }
    except Exception as e:
        print(f"Erro ao obter dados do dashboard: {str(e)}")
        return {
            "projects_summary": {
                "total_projects": 0,
                "active_projects": 0,
                "completed_projects": 0,
                "cancelled_projects": 0
            },
            "budget_summary": {
                "total_budget": 0,
                "total_spent": 0,
                "percentage": 0
            },
            "projects_by_type": [],
            "tasks_by_status": [],
            "materials_by_category": [],
            "monthly_progress": [],
            "quantity_clients": 0
        }
    finally:
        cursor.close()
        conn.close()

# Operações para Clientes de Paisagismo
def create_client(
    user_id: int,
    client_name: str,
    contact_person: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    address: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    zip_code: Optional[str] = None,
    client_type: Optional[str] = None,
    industry: Optional[str] = None,
    status: str = "Lead",
    last_interaction_date: Optional[str] = None,
    next_follow_up_date: Optional[str] = None,
    notes: Optional[str] = None,
    id_whatsapp: Optional[str] = None,
    img_profile: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um novo cliente de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO landscaping_crm_clients (
            user_id, client_name, contact_person, email, phone_number, 
            address, city, state, zip_code, client_type, industry, 
            status, last_interaction_date, next_follow_up_date, notes, id_whatsapp, img_profile
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        cursor.execute(query, (
            user_id, client_name, contact_person, email, phone_number,
            address, city, state, zip_code, client_type, industry,
            status, last_interaction_date, next_follow_up_date, notes, id_whatsapp, img_profile
        ))
        
        client_id = cursor.lastrowid
        conn.commit()
        
        # Buscar o registro recém-criado
        return get_client(client_id)
    except Exception as e:
        print(f"Erro ao criar cliente de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_clients(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todos os clientes de paisagismo com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros incluindo img_profile
        query = """
        SELECT id, user_id, client_name, contact_person, email, phone_number, 
               address, city, state, zip_code, client_type, industry, status, 
               last_interaction_date, next_follow_up_date, notes, id_whatsapp, 
               img_profile, created_at, updated_at 
        FROM landscaping_crm_clients WHERE 1=1
        """
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "client_name" in filters:
            query += " AND client_name LIKE %s"
            params.append(f"%{filters['client_name']}%")
            
        if "industry" in filters:
            query += " AND industry = %s"
            params.append(filters["industry"])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY client_name LIMIT %s OFFSET %s"
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter clientes de paisagismo: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_clients(filters: Dict[str, Any]) -> int:
    """
    Conta o total de clientes de paisagismo com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM landscaping_crm_clients WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "status" in filters:
            query += " AND status = %s"
            params.append(filters["status"])
        
        if "client_name" in filters:
            query += " AND client_name LIKE %s"
            params.append(f"%{filters['client_name']}%")
            
        if "industry" in filters:
            query += " AND industry = %s"
            params.append(filters["industry"])
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar clientes de paisagismo: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_client(client_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um cliente específico pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT id, user_id, client_name, contact_person, email, phone_number, 
               address, city, state, zip_code, client_type, industry, status, 
               last_interaction_date, next_follow_up_date, notes, id_whatsapp, 
               img_profile, created_at, updated_at 
        FROM landscaping_crm_clients WHERE id = %s
        """
        cursor.execute(query, (client_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter cliente de paisagismo: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_client(
    client_id: int,
    user_id: int,
    update_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Atualiza um cliente de paisagismo.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o cliente existe e pertence ao usuário
        check_query = "SELECT id FROM landscaping_crm_clients WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (client_id, user_id))
        if not cursor.fetchone():
            return None
        
        # Construir a consulta de atualização
        if not update_data:
            return get_client(client_id)
        
        query = "UPDATE landscaping_crm_clients SET "
        params = []
        
        for key, value in update_data.items():
            query += f"{key} = %s, "
            params.append(value)
        
        # Remover a vírgula final e adicionar a condição WHERE
        query = query[:-2] + " WHERE id = %s AND user_id = %s"
        params.extend([client_id, user_id])
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            return get_client(client_id)
        return None
    except Exception as e:
        print(f"Erro ao atualizar cliente de paisagismo: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_client_by_whatsapp_id(whatsapp_id: str) -> Optional[Dict[str, Any]]:
    """
    Busca um cliente pelo ID do WhatsApp
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT id, user_id, client_name, contact_person, email, phone_number, 
               address, city, state, zip_code, client_type, industry, status, 
               last_interaction_date, next_follow_up_date, notes, id_whatsapp, 
               img_profile, created_at, updated_at 
        FROM landscaping_crm_clients WHERE id_whatsapp = %s
        """
        cursor.execute(query, (whatsapp_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar cliente por WhatsApp ID: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def create_quote_item(
    quote_id: int,
    service_id: int,
    quantity: float,
    unit_price: float,
    subtotal: float,
    description: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Cria um novo item de orçamento.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        INSERT INTO landscaping_quote_items 
        (quote_id, service_id, quantity, unit_price, subtotal, description) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            quote_id, service_id, quantity, unit_price, subtotal, description
        ))
        
        item_id = cursor.lastrowid
        conn.commit()
        
        # Buscar o item criado com informações do serviço
        query_select = """
        SELECT qi.*, s.service_name, s.category
        FROM landscaping_quote_items qi
        JOIN landscaping_services s ON qi.service_id = s.id
        WHERE qi.id = %s
        """
        cursor.execute(query_select, (item_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao criar item de orçamento: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def update_quote_item(
    item_id: int,
    quote_id: int,
    update_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Atualiza um item específico de orçamento.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Verificar se o item existe
        check_query = "SELECT id FROM landscaping_quote_items WHERE id = %s AND quote_id = %s"
        cursor.execute(check_query, (item_id, quote_id))
        if not cursor.fetchone():
            return None
        
        # Construir query de atualização
        update_fields = []
        update_values = []
        
        for field in ["service_id", "quantity", "unit_price", "subtotal", "description"]:
            if field in update_data and update_data[field] is not None:
                update_fields.append(f"{field} = %s")
                update_values.append(update_data[field])
        
        if not update_fields:
            # Buscar o item atual se não há campos para atualizar
            query_select = """
            SELECT qi.*, s.service_name, s.category
            FROM landscaping_quote_items qi
            JOIN landscaping_services s ON qi.service_id = s.id
            WHERE qi.id = %s
            """
            cursor.execute(query_select, (item_id,))
            return cursor.fetchone()
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        update_query = f"UPDATE landscaping_quote_items SET {', '.join(update_fields)} WHERE id = %s AND quote_id = %s"
        update_values.extend([item_id, quote_id])
        
        cursor.execute(update_query, update_values)
        conn.commit()
        
        # Buscar o item atualizado
        query_select = """
        SELECT qi.*, s.service_name, s.category
        FROM landscaping_quote_items qi
        JOIN landscaping_services s ON qi.service_id = s.id
        WHERE qi.id = %s
        """
        cursor.execute(query_select, (item_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao atualizar item de orçamento: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def delete_quote_item(item_id: int, quote_id: int) -> bool:
    """
    Remove um item específico de orçamento.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o item existe
        check_query = "SELECT id FROM landscaping_quote_items WHERE id = %s AND quote_id = %s"
        cursor.execute(check_query, (item_id, quote_id))
        if not cursor.fetchone():
            return False
        
        # Remover o item
        delete_query = "DELETE FROM landscaping_quote_items WHERE id = %s AND quote_id = %s"
        cursor.execute(delete_query, (item_id, quote_id))
        conn.commit()
        
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover item de orçamento: {str(e)}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()