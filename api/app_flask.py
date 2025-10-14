from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers="*", supports_credentials=True)

# Configuração do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '72.60.140.128'),
    'user': os.getenv('DB_USER', 'eden'),
    'password': os.getenv('DB_PASSWORD', 'eden2025@!'),
    'database': os.getenv('DB_NAME', 'eden_db'),
    'port': int(os.getenv('DB_PORT', 2621))
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Erro ao conectar com o banco: {e}")
        return None

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

@app.route('/status')
def status():
    return jsonify({"status": "online", "version": "1.0.0", "message": "API is running correctly"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# Endpoints removidos - usando FastAPI landscaping.py

@app.route('/test-db')
def test_db():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return jsonify({"status": "success", "message": "Database connected successfully"})
        except Error as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        return jsonify({"status": "error", "message": "Failed to connect to database"}), 500

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)