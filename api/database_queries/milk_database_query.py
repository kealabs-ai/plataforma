import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
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
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
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
            
    def get_milk_price_history(self, page: int = 1, page_size: int = 6) -> Dict[str, Any]:
        """
        Obtém o histórico de preços do leite com paginação.
        
        Args:
            page: Número da página
            page_size: Tamanho da página
            
        Returns:
            Dicionário com os registros de preços e informações de paginação
        """
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Consulta para contar o total de registros
        count_query = "SELECT COUNT(*) as total FROM milk_price_history"
        cursor.execute(count_query)
        total_records = cursor.fetchone()['total']
        
        # Calcular total de páginas
        total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 1
        
        # Consulta para obter os registros da página atual
        query = """
        SELECT 
            id,
            state,
            record_date,
            net_price_avg,
            dairy_percentage,
            rural_producer_pair_price
        FROM 
            milk_price_history
        ORDER BY 
            record_date DESC
        LIMIT %s OFFSET %s
        """
        
        offset = (page - 1) * page_size
        cursor.execute(query, (page_size, offset))
        records = cursor.fetchall()
        
        # Formatar datas para strings ISO
        for record in records:
            if record.get('record_date'):
                record['record_date'] = record['record_date'].isoformat()
        
        cursor.close()
        
        return {
            "items": records,
            "page": page,
            "page_size": page_size,
            "total_items": total_records,
            "total_pages": total_pages
        }
    
    def get_current_milk_price(self) -> Dict[str, Any]:
        """
        Obtém o preço atual do leite e informações relacionadas.
        
        Returns:
            Dicionário com o preço atual do leite e informações relacionadas
        """
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Obter o registro mais recente
        query = """
        SELECT 
            id,
            state,
            record_date,
            net_price_avg,
            dairy_percentage,
            rural_producer_pair_price
        FROM 
            milk_price_history
        ORDER BY 
            record_date DESC
        LIMIT 1
        """
        
        cursor.execute(query)
        record = cursor.fetchone()
        
        if not record:
            # Se não houver registros, retornar valores padrão
            current_month = datetime.now().strftime('%Y-%m')
            return {
                "month": current_month,
                "net_price_avg": 2.50,
                "dairy_percentage": 0.15,
                "milk_price": 2.50
            }
        
        # Formatar data para string ISO
        if record.get('record_date'):
            record['record_date'] = record['record_date'].isoformat()
            record['month'] = record['record_date'][:7]  # Formato YYYY-MM
        
        # Calcular o preço final do leite
        milk_price = record['rural_producer_pair_price']
        
        # Adicionar o preço final ao registro
        record['milk_price'] = milk_price
        
        cursor.close()
        
        return record
    
    def update_milk_price(self, net_price_avg: float, dairy_percentage: float) -> Dict[str, Any]:
        """
        Atualiza o preço do leite para o último mês vigente.
        
        Args:
            net_price_avg: Preço médio líquido
            dairy_percentage: Percentual do laticínio
            
        Returns:
            Dicionário com o novo preço do leite e informações relacionadas
        """
        self.ensure_connection()
        cursor = self.connection.cursor(dictionary=True)
        
        # Calcular o preço final do leite
        rural_producer_pair_price = net_price_avg * (1 - dairy_percentage)
        
        # Obter o último mês vigente (registro mais recente)
        latest_query = """
        SELECT id, record_date FROM milk_price_history
        ORDER BY record_date DESC
        LIMIT 1
        """
        cursor.execute(latest_query)
        latest_record = cursor.fetchone()
        
        if latest_record:
            # Atualizar o registro mais recente
            update_query = """
            UPDATE milk_price_history
            SET net_price_avg = %s, dairy_percentage = %s, rural_producer_pair_price = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (net_price_avg, dairy_percentage, rural_producer_pair_price, latest_record['id']))
            record_date = latest_record['record_date']
        else:
            # Se não houver registros, criar um para o mês atual
            record_date = datetime.now().replace(day=1).date()
            insert_query = """
            INSERT INTO milk_price_history 
            (state, record_date, net_price_avg, dairy_percentage, rural_producer_pair_price)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, ('SP', record_date, net_price_avg, dairy_percentage, rural_producer_pair_price))
        
        self.connection.commit()
        cursor.close()
        
        # Retornar o preço atualizado
        return {
            "month": record_date.strftime('%Y-%m'),
            "net_price_avg": net_price_avg,
            "dairy_percentage": dairy_percentage,
            "rural_producer_pair_price": rural_producer_pair_price,
            "milk_price": rural_producer_pair_price
        }

milk_db_query = MilkDatabaseQuery()