import mysql.connector
from mysql.connector import Error
from datetime import date, datetime
from typing import Dict, List, Any, Optional
import os
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class BeefCattleDatabase:
    def __init__(self):
        self.connection = None
        self.connect()
    
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
        
    def create_beef_cattle(self, cattle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new beef cattle record
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            INSERT INTO beef_cattle (
                official_id, name, birth_date, breed, gender, 
                entry_date, entry_weight, current_weight, target_weight, 
                status, expected_finish_date, notes
            ) VALUES (
                %(official_id)s, %(name)s, %(birth_date)s, %(breed)s, %(gender)s,
                %(entry_date)s, %(entry_weight)s, %(current_weight)s, %(target_weight)s,
                %(status)s, %(expected_finish_date)s, %(notes)s
            )
            """
            
            # If current_weight is not provided, use entry_weight
            if not cattle_data.get('current_weight'):
                cattle_data['current_weight'] = cattle_data['entry_weight']
                
            cursor.execute(query, cattle_data)
            cattle_id = cursor.lastrowid
            self.connection.commit()
            
            # Get the created record
            cursor.execute("SELECT * FROM beef_cattle WHERE id = %s", (cattle_id,))
            result = cursor.fetchone()
            
            cursor.close()
            
            return result
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def count_beef_cattle(self, filters: Dict[str, Any] = None) -> int:
        """
        Count beef cattle records with optional filters
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            query = "SELECT COUNT(*) FROM beef_cattle WHERE 1=1"
            params = []
            
            if filters:
                if 'status' in filters:
                    query += " AND status = %s"
                    params.append(filters['status'])
                    
                if 'breed' in filters:
                    query += " AND breed = %s"
                    params.append(filters['breed'])
                    
                if 'min_weight' in filters:
                    query += " AND current_weight >= %s"
                    params.append(filters['min_weight'])
                    
                if 'max_weight' in filters:
                    query += " AND current_weight <= %s"
                    params.append(filters['max_weight'])
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            
            cursor.close()
            
            return count
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_all_beef_cattle(self, filters: Dict[str, Any] = None, page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get all beef cattle records with optional filters and pagination
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = "SELECT * FROM beef_cattle WHERE 1=1"
            params = []
            
            if filters:
                if 'status' in filters:
                    query += " AND status = %s"
                    params.append(filters['status'])
                    
                if 'breed' in filters:
                    query += " AND breed = %s"
                    params.append(filters['breed'])
                    
                if 'min_weight' in filters:
                    query += " AND current_weight >= %s"
                    params.append(filters['min_weight'])
                    
                if 'max_weight' in filters:
                    query += " AND current_weight <= %s"
                    params.append(filters['max_weight'])
            
            # Add pagination
            query += " ORDER BY id DESC LIMIT %s OFFSET %s"
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            
            return results
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_beef_cattle_by_id(self, cattle_id: int) -> Dict[str, Any]:
        """
        Get a specific beef cattle record by ID
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM beef_cattle WHERE id = %s", (cattle_id,))
            result = cursor.fetchone()
            
            cursor.close()
            
            return result
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def update_beef_cattle(self, cattle_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a beef cattle record
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            # Build the update query dynamically based on provided fields
            set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
            query = f"UPDATE beef_cattle SET {set_clause} WHERE id = %s"
            
            # Add values and cattle_id to params
            params = list(update_data.values())
            params.append(cattle_id)
            
            cursor.execute(query, params)
            self.connection.commit()
            
            # Check if record exists and was updated
            if cursor.rowcount == 0:
                cursor.close()
                return None
                
            # Get the updated record
            cursor.execute("SELECT * FROM beef_cattle WHERE id = %s", (cattle_id,))
            result = cursor.fetchone()
            
            cursor.close()
            
            return result
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def delete_beef_cattle(self, cattle_id: int) -> bool:
        """
        Delete a beef cattle record
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            cursor.execute("DELETE FROM beef_cattle WHERE id = %s", (cattle_id,))
            self.connection.commit()
            
            success = cursor.rowcount > 0
            
            cursor.close()
            
            return success
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def count_weight_records(self, filters: Dict[str, Any]) -> int:
        """
        Count weight records with filters
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            query = "SELECT COUNT(*) FROM beef_cattle_weights WHERE cattle_id = %s"
            params = [filters['cattle_id']]
            
            if 'start_date' in filters:
                query += " AND weight_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND weight_date <= %s"
                params.append(filters['end_date'])
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            
            cursor.close()
            
            return count
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def add_weight_record(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new weight record
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            INSERT INTO beef_cattle_weights (
                cattle_id, weight_date, weight, notes, user_id
            ) VALUES (
                %(cattle_id)s, %(weight_date)s, %(weight)s, %(notes)s, %(user_id)s
            )
            """
            
            cursor.execute(query, record_data)
            record_id = cursor.lastrowid
            self.connection.commit()
            
            # Get the created record
            cursor.execute("SELECT * FROM beef_cattle_weights WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            
            cursor.close()
            
            return result
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_weight_records(self, filters: Dict[str, Any], page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get weight records with filters and pagination
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = "SELECT * FROM beef_cattle_weights WHERE cattle_id = %s"
            params = [filters['cattle_id']]
            
            if 'start_date' in filters:
                query += " AND weight_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND weight_date <= %s"
                params.append(filters['end_date'])
                
            query += " ORDER BY weight_date ASC"
            
            # Add pagination
            query += " LIMIT %s OFFSET %s"
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            
            return results
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def count_feeding_records(self, filters: Dict[str, Any]) -> int:
        """
        Count feeding records with filters
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            query = "SELECT COUNT(*) FROM beef_cattle_feeding WHERE cattle_id = %s"
            params = [filters['cattle_id']]
            
            if 'start_date' in filters:
                query += " AND feeding_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND feeding_date <= %s"
                params.append(filters['end_date'])
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            
            cursor.close()
            
            return count
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def add_feeding_record(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new feeding record
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            INSERT INTO beef_cattle_feeding (
                cattle_id, feeding_date, feed_type, quantity, unit, notes, user_id
            ) VALUES (
                %(cattle_id)s, %(feeding_date)s, %(feed_type)s, %(quantity)s, 
                %(unit)s, %(notes)s, %(user_id)s
            )
            """
            
            cursor.execute(query, record_data)
            record_id = cursor.lastrowid
            self.connection.commit()
            
            # Get the created record
            cursor.execute("SELECT * FROM beef_cattle_feeding WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            
            cursor.close()
            
            return result
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_feeding_records(self, filters: Dict[str, Any], page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get feeding records with filters and pagination
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = "SELECT * FROM beef_cattle_feeding WHERE cattle_id = %s"
            params = [filters['cattle_id']]
            
            if 'start_date' in filters:
                query += " AND feeding_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND feeding_date <= %s"
                params.append(filters['end_date'])
                
            query += " ORDER BY feeding_date ASC"
            
            # Add pagination
            query += " LIMIT %s OFFSET %s"
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            
            return results
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def count_health_records(self, filters: Dict[str, Any]) -> int:
        """
        Count health records with filters
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            query = "SELECT COUNT(*) FROM beef_cattle_health WHERE cattle_id = %s"
            params = [filters['cattle_id']]
            
            if 'start_date' in filters:
                query += " AND record_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND record_date <= %s"
                params.append(filters['end_date'])
                
            if 'record_type' in filters:
                query += " AND record_type = %s"
                params.append(filters['record_type'])
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            
            cursor.close()
            
            return count
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def add_health_record(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new health record
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            INSERT INTO beef_cattle_health (
                cattle_id, record_date, record_type, description, 
                medicine, dosage, notes, user_id
            ) VALUES (
                %(cattle_id)s, %(record_date)s, %(record_type)s, %(description)s,
                %(medicine)s, %(dosage)s, %(notes)s, %(user_id)s
            )
            """
            
            cursor.execute(query, record_data)
            record_id = cursor.lastrowid
            self.connection.commit()
            
            # Get the created record
            cursor.execute("SELECT * FROM beef_cattle_health WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            
            cursor.close()
            
            return result
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_health_records(self, filters: Dict[str, Any], page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get health records with filters and pagination
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = "SELECT * FROM beef_cattle_health WHERE cattle_id = %s"
            params = [filters['cattle_id']]
            
            if 'start_date' in filters:
                query += " AND record_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND record_date <= %s"
                params.append(filters['end_date'])
                
            if 'record_type' in filters:
                query += " AND record_type = %s"
                params.append(filters['record_type'])
                
            query += " ORDER BY record_date DESC"
            
            # Add pagination
            query += " LIMIT %s OFFSET %s"
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            
            return results
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
    
    def count_sale_records(self, filters: Dict[str, Any]) -> int:
        """
        Count sale records with filters
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor()
            
            query = """
            SELECT COUNT(*) 
            FROM beef_cattle_sales s
            JOIN beef_cattle c ON s.cattle_id = c.id
            WHERE 1=1
            """
            params = []
            
            if 'start_date' in filters:
                query += " AND s.sale_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND s.sale_date <= %s"
                params.append(filters['end_date'])
            
            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            
            cursor.close()
            
            return count
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def add_sale_record(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new sale record
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            INSERT INTO beef_cattle_sales (
                cattle_id, sale_date, final_weight, price_per_kg, 
                total_value, buyer, notes, user_id
            ) VALUES (
                %(cattle_id)s, %(sale_date)s, %(final_weight)s, %(price_per_kg)s,
                %(total_value)s, %(buyer)s, %(notes)s, %(user_id)s
            )
            """
            
            cursor.execute(query, record_data)
            record_id = cursor.lastrowid
            self.connection.commit()
            
            # Get the created record
            cursor.execute("SELECT * FROM beef_cattle_sales WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            
            cursor.close()
            
            return result
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_sale_records(self, filters: Dict[str, Any], page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
        """
        Get sale records with filters and pagination
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT s.*, c.official_id, c.name 
            FROM beef_cattle_sales s
            JOIN beef_cattle c ON s.cattle_id = c.id
            WHERE 1=1
            """
            params = []
            
            if 'start_date' in filters:
                query += " AND s.sale_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND s.sale_date <= %s"
                params.append(filters['end_date'])
                
            query += " ORDER BY s.sale_date DESC"
            
            # Add pagination
            query += " LIMIT %s OFFSET %s"
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            
            return results
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_dashboard_summary(self) -> Dict[str, Any]:
        print("Fetching dashboard summary")
        """
        Get summary data for dashboard
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            summary = {}
            
            # Total cattle count
            cursor.execute("SELECT COUNT(*) as total FROM beef_cattle")
            summary['total_cattle'] = cursor.fetchone()['total']
            
            # Cattle by status
            cursor.execute("SELECT status, COUNT(*) as count FROM beef_cattle GROUP BY status")
            summary['cattle_by_status'] = cursor.fetchall()
            
            # Average weight
            cursor.execute("SELECT AVG(current_weight) as avg_weight FROM beef_cattle WHERE status = 'Em Engorda'")
            summary['average_weight'] = cursor.fetchone()['avg_weight']
            
            # Total sales this month
            current_month = datetime.now().strftime('%Y-%m-01')
            cursor.execute(
                "SELECT SUM(total_value) as total_sales FROM beef_cattle_sales WHERE sale_date >= %s",
                (current_month,)
            )
            result = cursor.fetchone()
            summary['monthly_sales'] = result['total_sales'] if result['total_sales'] else 0
            
            cursor.close()
            
            return summary
        except Error as e:
            raise Exception(f"Database error: {str(e)}")
            
    def get_weight_gain_data(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get weight gain data for dashboard
        """
        try:
            self.ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                c.id, c.official_id, c.name,
                MIN(w.weight_date) as first_date,
                MAX(w.weight_date) as last_date,
                (
                    SELECT weight FROM beef_cattle_weights 
                    WHERE cattle_id = c.id 
                    ORDER BY weight_date ASC LIMIT 1
                ) as initial_weight,
                (
                    SELECT weight FROM beef_cattle_weights 
                    WHERE cattle_id = c.id 
                    ORDER BY weight_date DESC LIMIT 1
                ) as current_weight,
                DATEDIFF(
                    MAX(w.weight_date), 
                    MIN(w.weight_date)
                ) as days,
                (
                    (SELECT weight FROM beef_cattle_weights 
                    WHERE cattle_id = c.id 
                    ORDER BY weight_date DESC LIMIT 1) -
                    (SELECT weight FROM beef_cattle_weights 
                    WHERE cattle_id = c.id 
                    ORDER BY weight_date ASC LIMIT 1)
                ) as weight_gain,
                (
                    (
                        (SELECT weight FROM beef_cattle_weights 
                        WHERE cattle_id = c.id 
                        ORDER BY weight_date DESC LIMIT 1) -
                        (SELECT weight FROM beef_cattle_weights 
                        WHERE cattle_id = c.id 
                        ORDER BY weight_date ASC LIMIT 1)
                    ) / 
                    GREATEST(DATEDIFF(
                        MAX(w.weight_date), 
                        MIN(w.weight_date)
                    ), 1)
                ) as daily_gain
            FROM 
                beef_cattle c
            JOIN 
                beef_cattle_weights w ON c.id = w.cattle_id
            WHERE 
                c.status = 'Em Engorda'
            """
            params = []
            
            if 'start_date' in filters:
                query += " AND w.weight_date >= %s"
                params.append(filters['start_date'])
                
            if 'end_date' in filters:
                query += " AND w.weight_date <= %s"
                params.append(filters['end_date'])
                
            query += " GROUP BY c.id, c.official_id, c.name"
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            cursor.close()
            
            return results
        except Error as e:
            raise Exception(f"Database error: {str(e)}")

# Create an instance of the database class
beef_cattle_db = BeefCattleDatabase()