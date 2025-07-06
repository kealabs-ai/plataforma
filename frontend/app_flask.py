from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests
import logging
from dotenv import load_dotenv

# Importando os blueprints
from dashboards import bp as dashboards_bp
from properties import bp as properties_bp
from activities_inputs import bp as activities_inputs_bp
from finance import bp as finance_bp
from operations import bp as operations_bp

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API
API_URL = os.getenv("API_URL", "http://api:8000")
print(f"Using API URL: {API_URL}")

app = Flask(__name__)
app.secret_key = "kognia_one_secret_key"
app.logger.setLevel(logging.DEBUG)

# Registrando os blueprints
app.register_blueprint(dashboards_bp, url_prefix='/dashboards')
app.register_blueprint(properties_bp, url_prefix='/properties')
app.register_blueprint(activities_inputs_bp, url_prefix='/activities_inputs')
app.register_blueprint(finance_bp, url_prefix='/finance')
app.register_blueprint(operations_bp, url_prefix='/operations')

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        app.logger.debug(f"Attempting login for user: {username}")
        app.logger.debug(f"API URL: {API_URL}")
        
        try:
            # Usando o formato correto para o OAuth2 password flow
            app.logger.debug("Sending request to API...")
            response = requests.post(
                f"{API_URL}/token",
                data={
                    "username": username,
                    "password": password
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            
            app.logger.debug(f"API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                app.logger.debug("Login successful")
                session['token'] = data.get('access_token')
                session['token_type'] = data.get('token_type')
                return redirect(url_for('dashboard'))
            else:
                app.logger.error(f"API Error: {response.status_code} - {response.text}")
                error = "Credenciais inválidas. Tente novamente."
        except Exception as e:
            app.logger.error(f"Connection Error: {str(e)}")
            error = f"Erro ao conectar com a API: {str(e)}"
    
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('dash_agro.html')

@app.route('/dash_agro')
def dash_agro():
    return render_template('dash_agro.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/visitor')
def visitor():
    return render_template('visitor.html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))

@app.route('/api-status')
def api_status():
    try:
        response = requests.get(f"{API_URL}/status")
        return {
            "api_url": API_URL,
            "status": "online" if response.status_code == 200 else "offline",
            "response": response.json() if response.status_code == 200 else None,
            "status_code": response.status_code
        }
    except Exception as e:
        return {
            "api_url": API_URL,
            "status": "error",
            "error": str(e)
        }

# Beef Cattle Mock Endpoints
@app.route('/api/beef_cattle_mock/dashboard/summary')
def beef_cattle_dashboard_summary():
    return {
        "total_cattle": 5,
        "cattle_by_status": [
            {"status": "Em Engorda", "count": 4},
            {"status": "Vendido", "count": 1}
        ],
        "average_weight": 460.0,
        "monthly_sales": 11700.00
    }

@app.route('/api/beef_cattle_mock/')
def beef_cattle_list():
    return [
        {
            "id": 1,
            "official_id": "BG001",
            "name": "Sultão",
            "birth_date": "2023-01-15",
            "breed": "Nelore",
            "gender": "M",
            "entry_date": "2024-01-10",
            "entry_weight": 380.5,
            "current_weight": 450.2,
            "target_weight": 550.0,
            "status": "Em Engorda",
            "expected_finish_date": "2024-12-15",
            "notes": "Animal saudável, boa conversão alimentar",
            "created_at": "2024-01-10T00:00:00",
            "updated_at": "2024-04-10T00:00:00"
        },
        {
            "id": 2,
            "official_id": "BG002",
            "name": "Trovão",
            "birth_date": "2023-02-20",
            "breed": "Angus",
            "gender": "M",
            "entry_date": "2024-01-15",
            "entry_weight": 410.0,
            "current_weight": 470.5,
            "target_weight": 580.0,
            "status": "Em Engorda",
            "expected_finish_date": "2024-11-20",
            "notes": "Cruzamento industrial, alto ganho diário",
            "created_at": "2024-01-15T00:00:00",
            "updated_at": "2024-04-15T00:00:00"
        }
    ]

@app.route('/api/beef_cattle_mock/sales')
def beef_cattle_sales():
    return [
        {
            "id": 1,
            "cattle_id": 5,
            "official_id": "BG005",
            "name": "Relâmpago",
            "sale_date": "2024-03-20",
            "final_weight": 520.0,
            "price_per_kg": 22.50,
            "total_value": 11700.00,
            "buyer": "Frigorífico São José",
            "notes": "Venda antecipada por bom desempenho",
            "user_id": 1,
            "created_at": "2024-03-20T00:00:00"
        }
    ]

@app.route('/api/beef_cattle_mock/dashboard/weight-gain')
def beef_cattle_weight_gain():
    return [
        {
            "id": 1,
            "official_id": "BG001",
            "name": "Sultão",
            "first_date": "2024-01-10",
            "last_date": "2024-04-10",
            "initial_weight": 380.5,
            "current_weight": 450.2,
            "days": 90,
            "weight_gain": 69.7,
            "daily_gain": 0.77
        },
        {
            "id": 2,
            "official_id": "BG002",
            "name": "Trovão",
            "first_date": "2024-01-15",
            "last_date": "2024-04-15",
            "initial_weight": 410.0,
            "current_weight": 470.5,
            "days": 90,
            "weight_gain": 60.5,
            "daily_gain": 0.67
        }
    ]

@app.route('/api/beef_cattle_direct_test')
def beef_cattle_direct_test():
    return {"message": "Direct beef cattle test endpoint is working"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True)