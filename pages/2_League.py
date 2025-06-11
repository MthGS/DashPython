import streamlit as st
import pandas as pd
import google.generativeai as genai
from serpapi import GoogleSearch 

st.set_page_config(
    page_title="Leagues",
    page_icon="🏆",
    layout="wide"
)

#API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Chave da API do Google não encontrada. Verifique seu arquivo .streamlit/secrets.toml")
    st.stop()

#FUNÇÕES
@st.cache_data
def load_data_from_csv(file_path="fc25data/all_players_update.csv"):
    """Carrega o CSV principal com os dados dos jogadores."""
    try:
        return pd.read_csv(file_path, index_col=0)
    except FileNotFoundError:
        st.error(f"Erro Crítico: Arquivo '{file_path}' não foi encontrado.")
        return None

#FUNÇÃO DE BUSCA DE IMAGEM
@st.cache_data
def get_league_logo(league_name):
    """Busca a URL do logo de uma liga usando a API da SerpApi."""
    with st.spinner(f"Buscando logo para a {league_name}..."):
        try:
            params = {
              "q": f"{league_name} official logo", 
              "engine": "google_images",          
              "ijn": "0",                         
              "api_key": st.secrets["SERPAPI_API_KEY"] 
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Pega a URL da primeira imagem encontrada
            if "images_results" in results and len(results["images_results"]) > 0:
                return results["images_results"][0]["original"]
            else:
                return None
        except Exception as e:
            st.warning(f"Não foi possível buscar o logo via SerpApi: {e}")
            return None

#"""Gera uma descrição da liga usando a IA do Gemini."""
@st.cache_data
def get_league_description_from_gemini(league_name):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    prompt = f"Escreva um resumo informativo em um único parágrafo sobre a liga de futebol '{league_name}', incluindo seu país, um ou dois times principais e um fato interessante. Responda em português do Brasil."
    with st.spinner(f"Gemini está resumindo a {league_name}..."):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.warning(f"Não foi possível obter a descrição da IA: {e}")
            return "Descrição da IA indisponível no momento."

#LÓGICA PRINCIPAL DO APP
df_leagues_data = load_data_from_csv()

if df_leagues_data is None:
    st.stop()

if "League" not in df_leagues_data.columns:
    st.error("Erro Fatal: A coluna 'League' não foi encontrada no arquivo CSV.")
    st.stop()

list_of_leagues = sorted(list(df_leagues_data["League"].astype(str).str.strip().replace('', pd.NA).dropna().unique()))

if not list_of_leagues:
    st.warning("Nenhuma liga válida foi encontrada nos dados para seleção.")
else:
    selected_league = st.sidebar.selectbox("Selecione a Liga", list_of_leagues)

    if selected_league:
        logo_col, info_col = st.columns([1, 4])
        
        with logo_col:
            # Chama a nova função de busca de logo
            logo_url = get_league_logo(selected_league)
            if logo_url:
                st.image(logo_url, caption="Logo da Liga")
            else:
                st.caption("Logo não encontrado.")

        with info_col:
            st.title(f"🏆 {selected_league}")
            league_summary = get_league_description_from_gemini(selected_league)
            st.markdown(league_summary)

        st.divider()

        st.subheader("Jogadores da Liga")
        league_specific_data_df = df_leagues_data[
            df_leagues_data["League"].astype(str).str.strip() == selected_league
        ]
        if not league_specific_data_df.empty:
            st.write(f"Exibindo {len(league_specific_data_df)} registros.")
            st.dataframe(league_specific_data_df, use_container_width=True)