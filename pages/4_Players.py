import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data
import matplotlib.pyplot as plt

df_data = pd.read_csv("fc25data/all_players_update.csv")
male = pd.read_csv("fc25data/male.csv")
female = pd.read_csv("fc25data/female.csv")

st.set_page_config(
    page_title="Players",
    page_icon="⚽",
    layout="wide"
)

st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")
 
df_data = st.session_state["data"]
Liga = df_data["League"].value_counts().index
League = st.sidebar.selectbox("Liga", Liga)

df_clube = df_data[df_data["League"] == League]
clubes = df_clube["Team"].value_counts().index
clube = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[df_data["Team"] == clube]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("jogador", players)

player_stats = df_data[df_data["Name"] == player].iloc[0]
#Localiza url no site EA FC25, falta adicionar .png no final, para carregar somente a imagem.
st.title(f"{player_stats["Name"]}")

st.markdown(f"**Liga:** {player_stats["League"]}")
st.markdown(f"**clube:** {player_stats["Team"]}")
st.markdown(f"**Posição:** {player_stats["Alternative positions"]}")
st.markdown(f"**Idade:** {player_stats["Age"]}")
st.markdown(f"**Overall:** {player_stats["OVR"]}")
st.markdown(f"**Link fonte:** {player_stats["url"]}") 

def bar_chart(player_stats):
    df_data = pd.read_csv(player_stats)
    player_names = [df_data['Name'] == player].tolist()
    stats = df_data['OVR'].tolist()

    plt.bar(player_names, stats)
    plt.xlabel("Name")
    plt.ylabel("OVR")
    plt.title("Player Stats")
    plt.xticks(rotation=45)
    st.pyplot()