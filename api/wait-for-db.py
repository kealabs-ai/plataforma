import time
import os
import pymysql

def wait_for_db():
    db_host = os.getenv("DB_HOST", "db")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "root_password")
    db_name = os.getenv("DB_NAME", "kognia_one_db")
    
    max_retries = 30
    retry_interval = 2
    
    for i in range(max_retries):
        try:
            print(f"Attempt {i+1}/{max_retries} to connect to database...")
            conn = pymysql.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name
            )
            conn.close()
            print("Database connection successful!")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            time.sleep(retry_interval)
    
    print("Max retries reached. Could not connect to database.")
    return False

if __name__ == "__main__":
    wait_for_db()