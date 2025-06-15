import os
import sys
import uvicorn

# Adiciona o diretório raiz ao path para importações relativas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Inicia a aplicação FastAPI
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)