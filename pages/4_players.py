import streamlit as st

df_data = st.session_state["data"]
clube = df_data["Team"].value_counts().index
team = st.sidebar.selectbox("Clube", clube)

df_players = df_data[df_data["Team"] == team]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("jogador", players)

player_stats = df_data[df_data["Name"] == player].iloc[0]
#Localiza url no site EA FC25, falta adicionar .png no final, para carregar somente a imagem.
st.image(player_stats["url"])
st.title(f"{player_stats["Name"]}")

st.markdown(f"**clube:** {player_stats["Team"]}")
st.markdown(f"**Posição:** {player_stats["Alternative positions"]}")