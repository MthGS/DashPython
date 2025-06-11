import streamlit as st
import pandas as pd
import pycountry
from auth import carregar_chaves_e_configurar_apis 

#CHAMA a função para obter as chaves/clientes
config_apis = carregar_chaves_e_configurar_apis()

st.set_page_config(
    page_title="FC 25 Data",
    page_icon="⚽",
    layout="wide"
)

male = pd.read_csv("fc25data/male.csv")
female = pd.read_csv("fc25data/female.csv")

#FUNÇÕES
# Função para converter o DataFrame para CSV (otimizada com cache)
@st.cache_data
def convert_df_to_csv(df):
   return df.to_csv(index=False).encode('utf-8')

# Função para buscar a URL da bandeira
@st.cache_data # Cache para não buscar a mesma bandeira várias vezes
def get_flag_url(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return f"https://flagcdn.com/w40/{country.alpha_2.lower()}.png"
    except Exception:
        pass # Se pycountry falhar, usa o fallback abaixo
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/BLANK_ICON.png/40px-BLANK_ICON.png"

#CARREGAMENTO DE DADOS
if "data" not in st.session_state:
    df_full = pd.read_csv("fc25data/all_players_update.csv", index_col=0)
    st.session_state["data"] = df_full
else:
    df_full = st.session_state["data"]

df_top10 = df_full.sort_values(by="Rank", ascending=True).head(10)


#LAYOUT
st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")
st.title("FC 25 DATA")
st.write("Based on eletronic arts EA FC25 data")

col1, col2 = st.columns(2)

#COLUNA DA ESQUERDA (Top 10 Jogadores)
with col1:
    st.markdown("""
        <style>
        /* Seu CSS aqui, sem alterações */
        .funnel-container { width: 100%; max-width: 700px; margin: auto; padding-top: 20px; }
        .funnel-step { background: linear-gradient(90deg, #1f77b4, #3fa9f5); color: white; padding: 16px; margin-bottom: 12px; border-radius: 30px; font-size: 18px; font-weight: 500; box-shadow: 2px 4px 10px rgba(0,0,0,0.1); text-align: left; display: flex; align-items: center; gap: 12px; transition: all 0.3s ease-in-out; }
        .funnel-step:hover { transform: scale(1.0); background: linear-gradient(90deg, #0d6efd, #00bfff); }
        .flag-icon { width: 33px; height: 22px; border-radius: 4px; object-fit: cover; }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("Top Players by OVR")
    
    st.markdown('<div class="funnel-container">', unsafe_allow_html=True)
    
    max_ovr = df_top10['OVR'].max()

    for _, row in df_top10.iterrows():
        largura = int((row['OVR'] / max_ovr) * 100)
        flag_url = get_flag_url(row.get('Nation', ''))
        
        st.markdown(f"""
            <div class="funnel-step" style="width: {largura}%;">
                <img class="flag-icon" src="{flag_url}" alt="{row.get('Nation', 'Unknown')}">
                <span>{row['Name']} ({row.get('Position', 'N/A')}) — OVR {row['OVR']}</span>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)


#COLUNA DA DIREITA (Média de Rank por OVR) #A decidir se vou manter essas métricas
with col2:
    st.subheader("Média de Rank por Nível de OVR")

    #Etiquetar os dados com o gênero, como antes.
    df_processed = df_full.copy()
    df_processed.loc[df_full['OVR'].isin(male['Rank']), 'Gender'] = 'Male'
    df_processed.loc[df_full['OVR'].isin(female['Rank']), 'Gender'] = 'Female'
    df_processed.dropna(subset=['Gender'], inplace=True)

    
    #Agrupamos por OVR e depois por Gênero.
    #Calculamos a média da coluna 'Rank' para cada um desses grupos.
    #O .unstack() transforma 'Male'/'Female' em colunas, ideal para o gráfico.
    count_by_ovr = df_processed.groupby(['OVR', 'Gender'])['OVR'].size().unstack(fill_value=0)

    #ABAS DE VISUALIZAÇÃO
    tab1, tab2 = st.tabs(["Gráfico de Linha (Tendência)", "Gráfico de Barras (Valores Exatos)"])

    with tab1:
        st.markdown("Ideal para ver a forma geral da distribuição e onde estão os picos.")
        #O Gráfico de Linha mostra a tendência da contagem de jogadores conforme o OVR aumenta
        st.line_chart(
            count_by_ovr,
            color=['#FFC0CB', '#0000FF'], # Rosa para Female, Azul para Male
            use_container_width=True
        )

    with tab2:
        st.markdown("Ideal para comparar a contagem exata em um nível de OVR específico.")
        #O Gráfico de Barras mostra a contagem exata de jogadores para cada OVR
        st.bar_chart(
            count_by_ovr,
            color=['#FFC0CB', '#0000FF'], # Rosa para Female, Azul para Male
            use_container_width=True
        )

    st.markdown("###### Tabela de Contagem de Jogadores por OVR:")
    st.dataframe(count_by_ovr, use_container_width=True)

    #Se um dia quiser ver a distribuição completa (mínimo, máximo, mediana),
    #um gráfico de caixa (box plot) também seria uma boa opção.
#FIM DO LAYOUT DA PÁGINA


#COLUNA DA DIREITA (Comparação de OVR Masculino vs. Feminino)    

st.header("All data in CSV file")
    
#Passo 1 - Pegar os valores mínimo e máximo do DataFrame completo
min_ovr = int(df_full['OVR'].min())
max_ovr = int(df_full['OVR'].max())

#Criar o slider de intervalo
selected_ovr_range = st.slider(
    "Selecione o intervalo de OVR (Overall Rating):",
    min_value=min_ovr,
    max_value=max_ovr,
    value=(min_ovr, max_ovr)  # O valor inicial é o intervalo completo
)

#Filtrar o DataFrame com base no intervalo do slider
# A condição verifica se o OVR está entre o valor mínimo e máximo do slider
df_filtered = df_full[
    (df_full['OVR'] >= selected_ovr_range[0]) &
    (df_full['OVR'] <= selected_ovr_range[1])
]

#Exibe o DataFrame filtrado
st.dataframe(df_filtered, use_container_width=True)

#O botão de download agora baixa os dados filtrados
csv_data = convert_df_to_csv(df_filtered)
st.download_button(
   label="Press to Download Filtered Data",
   data=csv_data,
   file_name="filtered_players.csv",
   mime="text/csv",
   key='download-csv'
)