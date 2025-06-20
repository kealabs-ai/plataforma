from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests
import logging
from dotenv import load_dotenv

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

@app.route('/')
def index():
    return redirect(url_for('login'))

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
    if 'token' not in session:
        return redirect(url_for('login'))
    
    # Get user info using the token
    try:
        response = requests.get(
            f"{API_URL}/users/me",
            headers={
                "Authorization": f"{session.get('token_type', 'Bearer')} {session.get('token')}"
            }
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return render_template('dashboard.html', user=user_data)
        else:
            # Token might be invalid or expired
            session.pop('token', None)
            session.pop('token_type', None)
            return redirect(url_for('login'))
    except Exception as e:
        app.logger.error(f"API Error: {str(e)}")
        return render_template('dashboard.html', error=str(e))

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True)