import pandas as pd
import streamlit as st
import altair as alt
from auth import carregar_chaves_e_configurar_apis

#CHAMA a função para obter as chaves/clientes
config_apis = carregar_chaves_e_configurar_apis()

# Carrega os dados uma vez
@st.cache_data
def load_data():
    df_all = pd.read_csv("fc25data/all_players_update.csv")
    male_ranks = pd.read_csv("fc25data/male.csv")
    female_ranks = pd.read_csv("fc25data/female.csv")

    #Gêneros
    # Primeiro, adicionamos a coluna 'Gender' ao DataFrame principal.
    df_all.loc[df_all['Rank'].isin(male_ranks['Rank']), 'Gender'] = 'Male'
    df_all.loc[df_all['Rank'].isin(female_ranks['Rank']), 'Gender'] = 'Female'
    
    return df_all

st.set_page_config(
    page_title="Times",
    page_icon="🛡️",
    layout="wide"
)
st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")

#Carregar os Dados
df_data = load_data()

#Menu Lateral
st.sidebar.header("Filtros")
leagues = sorted(df_data["League"].dropna().unique())
selected_league = st.sidebar.selectbox("Liga", leagues)

# Filtra os times baseados na liga selecionada
df_league_filtered = df_data[df_data["League"] == selected_league]
teams = sorted(df_league_filtered["Team"].dropna().unique())
selected_team = st.sidebar.selectbox("Clube", teams)

#Com a coluna "Gender", podemos filtrar de forma simples.
team_stats = df_data[df_data["Team"] == selected_team]
team_stats_male = team_stats[team_stats["Gender"] == "Male"]
team_stats_female = team_stats[team_stats["Gender"] == "Female"]

st.title(f"{selected_team}")
st.markdown(f"**Liga:** {selected_league}")
st.markdown(f"**Estatísticas de jogadores para times masculinos e femininos em {selected_team}:**")

#Exibe as tabelas de jogadores
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Jogadores Masculinos ({len(team_stats_male)})")
    st.dataframe(team_stats_male, hide_index=True)

with col2:
    st.subheader(f"Jogadoras Femininas ({len(team_stats_female)})")
    st.dataframe(team_stats_female, hide_index=True)


st.subheader("Desempenho dos Melhores Jogadores")

#A lista de métricas baseada no DataFrame filtrado 'team_stats'
numeric_cols = team_stats.select_dtypes(include=['number']).columns.tolist()
#Remove colunas que não são métricas de desempenho
metrics_to_exclude = ['Rank', 'OVR', 'Age', 'Weak foot', 'Skill moves']
performance_metrics = [col for col in numeric_cols if col not in metrics_to_exclude]


selected_metric = st.selectbox(
    "Selecione uma métrica de desempenho",
    options=performance_metrics,
)

if selected_metric:
    team_stats[selected_metric] = pd.to_numeric(
        team_stats[selected_metric], errors="coerce"
    )

    # Pega os 10 melhores jogadores, sem se preocupar com o gênero aqui
    top_players = team_stats.dropna(subset=[selected_metric]).nlargest(10, selected_metric)

    if not top_players.empty:
        chart = alt.Chart(top_players).mark_bar().encode(
            x=alt.X(selected_metric, title=selected_metric),
            y=alt.Y("Name", sort="-x", title="Jogador"),
            color=alt.Color("Gender", scale=alt.Scale(domain=['Male', 'Female'], range=['#4B98E1', '#E14B98'])),
            tooltip=["Name", "Gender", selected_metric]
        ).properties(
            title=f"Top 10 Jogadores em {selected_team} por {selected_metric}",
            width=800,
            height=400
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.markdown("**Não há dados disponíveis para a métrica selecionada.**")
