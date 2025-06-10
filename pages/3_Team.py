import streamlit as st
import pandas as pd
import altair as alt

# Load the CSV files
df_data = pd.read_csv("fc25data/all_players.csv", index_col=0)
male = pd.read_csv("fc25data/male_players.csv", index_col=0)
female = pd.read_csv("fc25data/female_players.csv", index_col=0)

# Set up the Streamlit page configuration
st.set_page_config(
    page_title="Times",
    page_icon="🛡️",
    layout="wide"
)

st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")

# Use o df_data carregado diretamente
#df_data = st.session_state["data"]
Liga = df_data["League"].value_counts().index
League = st.sidebar.selectbox("Liga", Liga)

df_clube = df_data[df_data["League"] == League]
# clubes = df_clube["Team"].value_counts().index
clubes = sorted(df_clube["Team"].dropna().unique())
team = st.sidebar.selectbox("Clube", clubes)

# Filter data for the selected team
team_stats_male = male[male["Team"] == team]
team_stats_female = female[female["Team"] == team]

# Padding to match DataFrame sizes
max_rows = max(len(team_stats_male), len(team_stats_female))
if len(team_stats_male) < max_rows:
    padding = pd.DataFrame([[""] * len(team_stats_male.columns)] * (max_rows - len(team_stats_male)), columns=team_stats_male.columns)
    team_stats_male = pd.concat([team_stats_male, padding], ignore_index=True)

if len(team_stats_female) < max_rows:
    padding = pd.DataFrame([[""] * len(team_stats_female.columns)] * (max_rows - len(team_stats_female)), columns=team_stats_female.columns)
    team_stats_female = pd.concat([team_stats_female, padding], ignore_index=True)

# Combine male and female data for visualization
team_stats_male["Gender"] = "Male"
team_stats_female["Gender"] = "Female"
team_stats_combined = pd.concat([team_stats_male, team_stats_female], ignore_index=True)

# Display team title and league information
st.title(f"{team}")
# Use a liga do df_clube, que já foi filtrado
st.markdown(f"**Liga:** {League}")
st.markdown(f"**Estatísticas de jogadores para times masculinos e femininos em {team}:**")

# Create two columns for male and female players
#col1, col2 = st.columns(2, gap="large")  # Equal widths for both columns

#with col1:
#    st.subheader("Jogadores Masculinos")
#    st.dataframe(team_stats_male.iloc[:, 3:], height=200)  # Display male players' data
#
#with col2:
#    st.subheader("Jogadoras Femininas")
#    st.dataframe(team_stats_female.iloc[:, 3:], height=200)  # Display female players' data

# Add a graph for player performance
st.subheader("Desempenho dos Melhores Jogadores")
performance_metric = st.selectbox(
    "Selecione uma métrica de desempenho",
    options=team_stats_combined.columns[3:],  # Metrics assumed to start at column 3
)

# Ensure the selected metric column is numeric
if performance_metric:
    team_stats_combined[performance_metric] = pd.to_numeric(
        team_stats_combined[performance_metric], errors="coerce"
    )  # Convert to numeric, invalid values become NaN

    top_players = team_stats_combined.dropna(subset=[performance_metric]).nlargest(10, performance_metric)

    if not top_players.empty:
        chart = alt.Chart(top_players).mark_bar().encode(
            x=alt.X(performance_metric, title=performance_metric),
            y=alt.Y("Name", sort="-x", title="Jogador"),
            color="Gender",
            tooltip=["Name", "Gender", performance_metric]
        ).properties(
            title=f"Top 10 Jogadores em {team} por {performance_metric}",
            width=800,
            height=400
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.markdown("**Não há dados disponíveis para a métrica selecionada.**")