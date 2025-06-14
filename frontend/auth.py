import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da API
API_URL = os.getenv("API_URL", "http://localhost:8000")

def load_css():
    """Carrega CSS personalizado e Semantic UI"""
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">
    <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>
    """, unsafe_allow_html=True)
    
    # Carrega o CSS personalizado do arquivo
    css_file = os.path.join(os.path.dirname(__file__), "static", "css", "auth.css")
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def login_user(username, password):
    """Autentica o usuário via API"""
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        return None

def login_page():
    """Renderiza a página de login"""
    load_css()
    
    # Caminho para o logo (pode ser configurado para ser customizável)
    logo_image_path = os.path.join(os.path.dirname(__file__), "static", "images", "logo.png")
    logo_src = logo_image_path if os.path.exists(logo_image_path) else "https://via.placeholder.com/300x200?text=Logo+Kognia"
    
    # Container principal
    html_content = f"""
    <div class="login-container">
        <div class="login-box">
            <div class="logo-container">
                <img src="{logo_src}" alt="Logo da empresa" style="max-width: 100%; max-height: 300px;">
            </div>
            <div class="form-container">
                <h2 class="ui header">Login</h2>
                <div class="ui form">
                    <div class="field">
                        <label>Usuário</label>
                        <div class="ui left icon input">
                            <input type="text" id="auth_username" placeholder="Nome de usuário">
                            <i class="user icon"></i>
                        </div>
                    </div>
                    <div class="field">
                        <label>Senha</label>
                        <div class="ui left icon input">
                            <input type="password" id="auth_password" placeholder="Senha">
                            <i class="lock icon"></i>
                        </div>
                    </div>
                    <button class="ui primary fluid button" id="auth-login-btn">Entrar</button>
                    
                    <div class="links-container">
                        <a href="#" id="auth-forgot-password"><i class="key icon"></i> Esqueci minha senha</a>
                        <a href="#" id="auth-visitor-link"><i class="external alternate icon"></i> Área de visitantes</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const loginBtn = document.getElementById('auth-login-btn');
        if (loginBtn) {{
            loginBtn.addEventListener('click', function() {{
                const usernameInput = document.getElementById('auth_username');
                const passwordInput = document.getElementById('auth_password');
                
                if (usernameInput && passwordInput) {{
                    const username = usernameInput.value;
                    const password = passwordInput.value;
                    
                    window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        key: 'auth_form_data', // Key for Streamlit to identify the component
                        value: JSON.stringify({{
                            action: 'login',
                            username: username,
                            password: password
                        }})
                    }}, '*');
                }}
            }});
        }}

        const forgotPasswordLink = document.getElementById('auth-forgot-password');
        if (forgotPasswordLink) {{
            forgotPasswordLink.addEventListener('click', function(event) {{
                event.preventDefault();
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    key: 'auth_form_data',
                    value: JSON.stringify({{ action: 'forgot_password' }})
                }}, '*');
            }});
        }}
        
        const visitorLink = document.getElementById('auth-visitor-link');
        if (visitorLink) {{
            visitorLink.addEventListener('click', function(event) {{
                event.preventDefault();
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    key: 'auth_form_data',
                    value: JSON.stringify({{ action: 'visitor_area' }})
                }}, '*');
            }});
        }}
    }});
    </script>
    """
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Use a hidden text input to receive data from the JavaScript postMessage.
    # The 'key' here must match the 'key' in the JavaScript postMessage.
    # Initialize with an empty JSON object string.
    component_data_json = st.text_input(
        "auth_form_data_receiver", 
        key="auth_form_data",  # This key is targeted by JS
        label_visibility="collapsed", 
        value="{}"
    )
    
    if component_data_json and component_data_json != "{}":
        try:
            value = json.loads(component_data_json)
            
            if value.get('action') == 'login':
                username = value.get('username')
                password = value.get('password')
                
                if username and password:
                    result = login_user(username, password)
                    if result:
                        st.session_state.token = result.get('access_token')
                        st.session_state.logged_in = True
                        st.session_state.auth_form_data = "{}" # Reset after processing
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas. Tente novamente.")
                        st.session_state.auth_form_data = "{}" # Reset
            
            elif value.get('action') == 'forgot_password':
                st.session_state.page = 'forgot_password'
                st.session_state.auth_form_data = "{}" # Reset
                st.rerun()
            
            elif value.get('action') == 'visitor_area':
                st.session_state.page = 'visitor'
                st.session_state.auth_form_data = "{}" # Reset
                st.rerun()
                
        except json.JSONDecodeError:
            st.warning("Falha ao processar dados do formulário.")
            st.session_state.auth_form_data = "{}" # Reset on error
        except Exception as e:
            st.error(f"Ocorreu um erro: {str(e)}")
            st.session_state.auth_form_data = "{}" # Reset on error

def forgot_password_page():
    """Página de recuperação de senha"""
    load_css()
    st.title("Recuperação de Senha")
    
    email = st.text_input("Digite seu e-mail cadastrado")
    
    if st.button("Enviar link de recuperação"):
        # Implementar chamada à API para recuperação de senha
        st.success("Se o e-mail estiver cadastrado, você receberá um link para redefinir sua senha.")
    
    if st.button("Voltar ao login"):
        st.session_state.page = 'login'
        st.rerun()

def visitor_page():
    """Página para visitantes"""
    load_css()
    st.title("Área de Visitantes")
    
    st.write("Bem-vindo à plataforma Kognia One!")
    st.write("Aqui você pode explorar algumas funcionalidades disponíveis para visitantes.")
    
    # Conteúdo para visitantes
    st.subheader("Recursos disponíveis")
    st.write("- Demonstrações interativas")
    st.write("- Informações sobre a plataforma")
    st.write("- Contato para mais informações")
    
    if st.button("Voltar ao login"):
        st.session_state.page = 'login'
        st.rerun()

def auth_main():
    """Função principal de autenticação"""
    # Inicializa o estado da sessão
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    # Roteamento de páginas
    if st.session_state.logged_in:
        return True
    else:
        if st.session_state.page == 'login':
            login_page()
        elif st.session_state.page == 'forgot_password':
            forgot_password_page()
        elif st.session_state.page == 'visitor':
            visitor_page()
        return False

if __name__ == "__main__":
    auth_main()