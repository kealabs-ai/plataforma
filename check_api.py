import requests
import os
from dotenv import load_dotenv
import sys

def check_api_connection():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Obtém a URL da API do ambiente ou usa o padrão
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    print(f"Verificando conexão com a API em: {api_url}")
    
    try:
        # Tenta acessar o endpoint de status da API
        response = requests.get(f"{api_url}/status", timeout=5)
        response.raise_for_status()
        
        # Se chegou aqui, a conexão foi bem-sucedida
        print(f"✅ Conexão bem-sucedida!")
        print(f"Resposta da API: {response.json()}")
        return True
        
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Erro de conexão: Não foi possível conectar à API em {api_url}")
        print(f"Detalhes do erro: {str(e)}")
        print("\nPossíveis soluções:")
        print("1. Verifique se a API está em execução (execute 'run_api.bat')")
        print("2. Verifique se a URL da API está correta no arquivo .env")
        print("3. Se estiver usando Docker, verifique se os containers estão em execução")
        print("4. Verifique se não há firewall ou proxy bloqueando a conexão")
        
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: A API em {api_url} não respondeu a tempo")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP: {e}")
        
    except Exception as e:
        print(f"❌ Erro desconhecido: {str(e)}")
    
    return False

if __name__ == "__main__":
    # Executa a verificação
    success = check_api_connection()
    
    # Sai com código de erro se a conexão falhou
    if not success:
        sys.exit(1)