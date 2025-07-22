"""
Módulo de acesso ao banco de dados para o sistema de floricultura.
Implementa as operações CRUD para cultivos de flores, estufas e fornecedores.
"""

from typing import Dict, Any, List, Optional
from datetime import date
from data.connection import *

# ------------------- FLOWER CULTIVATION -------------------

def create_flower_cultivation(
    user_id: int,
    species: str,
    variety: Optional[str],
    planting_date: date,
    quantity: Optional[int],
    area_m2: float,
    greenhouse_id: Optional[int],
    expected_harvest_date: Optional[date],
    status: str = "active",
    notes: Optional[str] = None,
    image_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um novo registro de cultivo de flores.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            INSERT INTO flower_cultivation (
                user_id, species, variety, planting_date, quantity, area_m2, greenhouse_id,
                expected_harvest_date, status, notes, image_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, species, variety, planting_date, quantity, area_m2, greenhouse_id,
            expected_harvest_date, status, notes, image_url
        ))
        conn.commit()
        flower_id = cursor.lastrowid
        
        # Buscar o registro recém-criado
        return get_flower_cultivation(flower_id)
    except Exception as e:
        print(f"Erro ao criar cultivo de flores: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_flower_cultivations(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todos os registros de cultivo de flores com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = "SELECT * FROM flower_cultivation WHERE 1=1"
        params = []
        
        for key, value in filters.items():
            query += f" AND {key} = %s"
            params.append(value)
        
        # Adicionar ordenação e paginação
        query += " ORDER BY planting_date DESC LIMIT %s OFFSET %s"
        params.extend([page_size, (page - 1) * page_size])
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter cultivos de flores: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_flower_cultivations(filters: Dict[str, Any]) -> int:
    """
    Conta o total de registros de cultivo de flores com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM flower_cultivation WHERE 1=1"
        params = []
        
        for key, value in filters.items():
            query += f" AND {key} = %s"
            params.append(value)
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar cultivos de flores: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_flower_cultivation(flower_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém um registro específico de cultivo de flores pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM flower_cultivation WHERE id = %s", (flower_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter cultivo de flores: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

# ------------------- GREENHOUSES -------------------

def create_greenhouse(
    user_id: int,
    name: str,
    area_m2: float,
    type: str,
    temperature_control: bool = False,
    humidity_control: bool = False,
    irrigation_system: bool = False,
    location: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria uma nova estufa.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            INSERT INTO greenhouses (
                user_id, name, area_m2, type, temperature_control, humidity_control,
                irrigation_system, location, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, name, area_m2, type, temperature_control, humidity_control,
            irrigation_system, location, notes
        ))
        conn.commit()
        greenhouse_id = cursor.lastrowid
        
        # Buscar o registro recém-criado
        cursor.execute("SELECT * FROM greenhouses WHERE id = %s", (greenhouse_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao criar estufa: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_greenhouses(
    filters: Dict[str, Any],
    page: int = 1,
    page_size: int = 10
) -> List[Dict[str, Any]]:
    """
    Obtém todas as estufas com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = "SELECT * FROM greenhouses WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "type" in filters:
            query += " AND type = %s"
            params.append(filters["type"])
        
        # Adicionar ordenação e paginação
        query += " ORDER BY name LIMIT %s OFFSET %s"
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao obter estufas: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_greenhouses(filters: Dict[str, Any]) -> int:
    """
    Conta o total de estufas com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM greenhouses WHERE 1=1"
        params = []
        
        if "user_id" in filters:
            query += " AND user_id = %s"
            params.append(filters["user_id"])
        
        if "type" in filters:
            query += " AND type = %s"
            params.append(filters["type"])
        
        cursor.execute(query, params)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar estufas: {str(e)}")
        return 0
    finally:
        cursor.close()
        conn.close()

def get_greenhouse(greenhouse_id: int) -> Optional[Dict[str, Any]]:
    """
    Obtém uma estufa específica pelo ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = "SELECT * FROM greenhouses WHERE id = %s"
        cursor.execute(query, (greenhouse_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter estufa: {str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

def update_greenhouse(
    greenhouse_id: int,
    user_id: int,
    update_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Atualiza uma estufa.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se a estufa existe e pertence ao usuário
        check_query = "SELECT id FROM greenhouses WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (greenhouse_id, user_id))
        if not cursor.fetchone():
            return None
        
        # Construir a consulta de atualização
        if not update_data:
            return get_greenhouse(greenhouse_id)
        
        query = "UPDATE greenhouses SET "
        params = []
        
        for key, value in update_data.items():
            query += f"{key} = %s, "
            params.append(value)
        
        # Remover a vírgula final e adicionar a condição WHERE
        query = query[:-2] + " WHERE id = %s AND user_id = %s"
        params.extend([greenhouse_id, user_id])
        
        cursor.execute(query, params)
        conn.commit()
        
        if cursor.rowcount > 0:
            return get_greenhouse(greenhouse_id)
        return None
    except Exception as e:
        print(f"Erro ao atualizar estufa: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def delete_greenhouse(greenhouse_id: int, user_id: int) -> bool:
    """
    Remove uma estufa.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM greenhouses WHERE id = %s AND user_id = %s"
        cursor.execute(query, (greenhouse_id, user_id))
        conn.commit()
        
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover estufa: {str(e)}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# ------------------- SUPPLIERS -------------------

def create_supplier(
    user_id: int,
    name: str,
    contact_person: str,
    phone: str,
    email: str,
    products: str,
    last_purchase: Optional[date] = None,
    status: str = "Ativo",
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cria um novo fornecedor.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            INSERT INTO floriculture_suppliers (
                user_id, name, contact_person, phone, email, products,
                last_purchase, status, notes
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, name, contact_person, phone, email, products,
            last_purchase, status, notes
        ))
        conn.commit()
        supplier_id = cursor.lastrowid
        
        # Buscar o registro recém-criado
        cursor.execute("SELECT * FROM floriculture_suppliers WHERE id = %s", (supplier_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao criar fornecedor: {str(e)}")
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
    Obtém todos os fornecedores com filtros e paginação.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Construir a consulta com filtros
        query = "SELECT * FROM floriculture_suppliers WHERE 1=1"
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
        print(f"Erro ao obter fornecedores: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def count_suppliers(filters: Dict[str, Any]) -> int:
    """
    Conta o total de fornecedores com filtros.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Construir a consulta com filtros
        query = "SELECT COUNT(*) FROM floriculture_suppliers WHERE 1=1"
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
        print(f"Erro ao contar fornecedores: {str(e)}")
        return 0
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
        query = "SELECT * FROM floriculture_suppliers WHERE id = %s"
        cursor.execute(query, (supplier_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao obter fornecedor: {str(e)}")
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
    Atualiza um fornecedor.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Verificar se o fornecedor existe e pertence ao usuário
        check_query = "SELECT id FROM floriculture_suppliers WHERE id = %s AND user_id = %s"
        cursor.execute(check_query, (supplier_id, user_id))
        if not cursor.fetchone():
            return None
        
        # Construir a consulta de atualização
        if not update_data:
            return get_supplier(supplier_id)
        
        query = "UPDATE floriculture_suppliers SET "
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
        print(f"Erro ao atualizar fornecedor: {str(e)}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def delete_supplier(supplier_id: int, user_id: int) -> bool:
    """
    Remove um fornecedor.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM floriculture_suppliers WHERE id = %s AND user_id = %s"
        cursor.execute(query, (supplier_id, user_id))
        conn.commit()
        
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao remover fornecedor: {str(e)}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()