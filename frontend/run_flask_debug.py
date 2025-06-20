import debugpy
import os
import sys
from app_flask import app

def main():
    # Habilitar o debugger remoto
    debugpy.listen(("0.0.0.0", 5678))
    print("🔍 Debugger está ouvindo na porta 5678 (mapeada para 5679 externamente)")
    
    # Verificar se estamos em modo de debug
    if os.environ.get("DEBUG") == "1":
        print("🐞 Modo de debug ativado")
        print("💡 Para conectar um debugger, use a porta 5679 no host")
    
    # Iniciar o Flask em modo debug
    print("🚀 Iniciando Flask na porta 8501")
    app.run(host='0.0.0.0', port=8501, debug=True, use_reloader=True)

if __name__ == "__main__":
    sys.exit(main())