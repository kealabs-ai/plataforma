import debugpy
import os
import sys
import subprocess

def main():
    # Habilitar o debugger remoto
    debugpy.listen(("0.0.0.0", 5678))
    print("🔍 Debugger está ouvindo na porta 5678 (mapeada para 5679 externamente)")
    
    # Verificar se estamos em modo de debug
    if os.environ.get("DEBUG") == "1":
        print("🐞 Modo de debug ativado")
        print("💡 Para conectar um debugger, use a porta 5679 no host")
    
    # Iniciar o Streamlit com argumentos de debug
    cmd = [
        "streamlit", "run", "login.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
        "--server.runOnSave=true",
        "--logger.level=debug"
    ]
    
    print(f"🚀 Iniciando Streamlit: {' '.join(cmd)}")
    process = subprocess.run(cmd)
    return process.returncode

if __name__ == "__main__":
    sys.exit(main())