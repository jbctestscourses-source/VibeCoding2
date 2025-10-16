# run_app.py - Versão Definitiva (Corrige o AttributeError e o 404)

import os
import sys
from dotenv import load_dotenv

# --- INJEÇÃO DE CORREÇÕES CRÍTICAS PARA PYINSTALLER ---
import streamlit

# 1. CORREÇÃO DE METADADOS: Injeta a versão para evitar PackageNotFoundError.
# Esta correção é crucial e deve permanecer, pois resolve o erro mais difícil.
streamlit.__version__ = "1.99.9"

# 2. CORREÇÃO DE 404: Define a variável de ambiente para o caminho dos assets estáticos.
# Esta variável é lida pelo Streamlit no startup para encontrar a pasta 'static'.
# O caminho deve apontar para o diretório "streamlit" dentro da pasta dist/GeradorUserStories.
resources_path = os.path.join(os.path.dirname(sys.executable), "streamlit")
os.environ["STREAMLIT_STATIC_FOLDER"] = resources_path
# --- FIM DA INJEÇÃO ---

# Importação do bootstrap
import streamlit.web.bootstrap as st_web_bootstrap 


STREAMLIT_SCRIPT_NAME = "app.py"

def run_streamlit_app():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)

    # Manipulação do Path (Crucial para o .env e script)
    os.chdir(base_path) 
    
    dotenv_path = os.path.join(base_path, '.env')
    load_dotenv(dotenv_path=dotenv_path)

    if base_path not in sys.path:
        sys.path.append(base_path)

    # Usa o path completo (necessário para o bootstrap)
    streamlit_file_path = os.path.join(base_path, STREAMLIT_SCRIPT_NAME)
    
    # Inicialização Direta
    try:
        print("A iniciar a aplicação Streamlit...")
        
        st_web_bootstrap.run(
            streamlit_file_path, 
            is_hello=False,
            args=[
                '--server.port', '8501', 
                '--server.address', '0.0.0.0',
                '--browser.gatherUsageStats', 'false' 
            ], 
            flag_options={}
        )

    except SystemExit as e:
        if e.code != 0:
            print(f"A aplicação Streamlit terminou com código de erro: {e.code}")
            input("Prima Enter para fechar...")
        sys.exit(e.code)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        input(f"Ocorreu um erro inesperado: {e}\nPrima Enter para fechar...")
        sys.exit(1)

if __name__ == '__main__':
    run_streamlit_app()