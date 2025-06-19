import streamlit as st
import requests
import os
from dotenv import load_dotenv
from workflows import workflow_page

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Kognia One",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega CSS personalizado do Semantic UI
def load_css():
    # Carrega Semantic UI do CDN (fallback caso os arquivos locais não existam)
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">
    <script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>
    """, unsafe_allow_html=True)
    
    # Carrega CSS personalizado
    css_file = os.path.join(os.path.dirname(__file__), "static", "custom.css")
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Função para chamar a API
def call_api(endpoint, method="GET", data=None):
    api_url = os.getenv("API_URL", "http://localhost:8000")
    url = f"{api_url}/{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao chamar API: {str(e)}")
        return None

# Sidebar para navegação
def sidebar():
    with st.sidebar:
        logo_path = os.path.join(os.path.dirname(__file__), "static", "images", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)
        else:
            st.title("Kognia One")
        
        menu_option = st.radio(
            "Menu",
            ["Dashboard", "Assistente IA", "Workflows", "Configurações", "Sobre"]
        )
        
        st.markdown("---")
        st.markdown("© 2023 Kognia")
        
        return menu_option

# Páginas da aplicação
def dashboard_page():
    st.title("Dashboard Kognia One")
    st.write("Bem-vindo à plataforma Kognia One!")
    
    # Exemplo de cards usando Semantic UI
    st.markdown("""
    <div class="ui three cards">
        <div class="ui card">
            <div class="content">
                <div class="header">Assistente IA</div>
                <div class="description">Acesse o assistente inteligente</div>
            </div>
            <div class="ui bottom attached button">
                Acessar
            </div>
        </div>
        <div class="ui card">
            <div class="content">
                <div class="header">Análise de Dados</div>
                <div class="description">Visualize insights dos seus dados</div>
            </div>
            <div class="ui bottom attached button">
                Visualizar
            </div>
        </div>
        <div class="ui card">
            <div class="content">
                <div class="header">Configurações</div>
                <div class="description">Personalize sua experiência</div>
            </div>
            <div class="ui bottom attached button">
                Configurar
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def ai_assistant_page():
    st.title("Assistente IA")
    
    # Seleção do modelo de IA
    model = st.selectbox(
        "Escolha o modelo de IA",
        ["OpenAI GPT", "Google Gemini", "Anthropic Claude", "Llama", "Grok"]
    )
    
    # Área de chat
    st.markdown('<div class="ui segment chat-container"></div>', unsafe_allow_html=True)
    
    # Input do usuário
    user_input = st.text_input("Digite sua mensagem:")
    
    if st.button("Enviar"):
        if user_input:
            # Chamada à API para processar a mensagem
            response = call_api(
                "llm/generate", 
                method="POST", 
                data={"prompt": user_input, "model": model}
            )
            
            if response:
                st.write(f"Resposta: {response['response']}")

def settings_page():
    st.title("Configurações")
    
    # Configurações de tema
    st.subheader("Personalização")
    theme = st.selectbox("Tema", ["Claro", "Escuro", "Sistema"])
    
    # Configurações de modelo de IA padrão
    st.subheader("Modelo de IA Padrão")
    default_model = st.selectbox(
        "Modelo padrão",
        ["OpenAI GPT", "Google Gemini", "Anthropic Claude", "Llama", "Grok"]
    )
    
    if st.button("Salvar Configurações"):
        st.success("Configurações salvas com sucesso!")

def about_page():
    st.title("Sobre a Kognia One")
    
    st.markdown("""
    ## Plataforma Kognia One
    
    A Kognia One é uma plataforma integrada que utiliza múltiplos modelos de IA para fornecer
    soluções inteligentes e personalizadas para sua empresa.
    
    ### Recursos
    
    - Integração com múltiplos modelos de IA
    - Interface personalizável
    - Agentes inteligentes para automação
    - Análise avançada de dados
    
    ### Contato
    
    Para mais informações, entre em contato conosco pelo email: contato@kognia.com
    """)

# Função principal
def main():
    load_css()
    menu_option = sidebar()
    
    if menu_option == "Dashboard":
        dashboard_page()
    elif menu_option == "Assistente IA":
        ai_assistant_page()
    elif menu_option == "Workflows":
        workflow_page()
    elif menu_option == "Configurações":
        settings_page()
    elif menu_option == "Sobre":
        about_page()

if __name__ == "__main__":
    main()