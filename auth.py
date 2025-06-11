# auth.py

import streamlit as st
import openai
# Importe outras bibliotecas de API aqui, se necessário

def carregar_chaves_e_configurar_apis():
    """
    Carrega as chaves de API do Streamlit Secrets e configura os clientes das APIs.
    Retorna um dicionário com os clientes ou as chaves.
    """
    try:
        # Carrega as chaves do cofre do Streamlit
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        google_api_key = st.secrets["GOOGLE_API_KEY"]
        serpapi_api_key = st.secrets["SERPAPI_API_KEY"]

        # Você pode retornar as chaves ou clientes configurados
        return {
            "openai": openai, # Retorna o módulo já configurado
            "google_key": google_api_key,
            "serpapi_key": serpapi_api_key
        }

    except KeyError as e:
        st.error(f"Erro: A chave de API {e} não foi encontrada. Verifique seus segredos no Streamlit Cloud.")
        st.stop()
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao carregar as chaves: {e}")
        st.stop()