import streamlit as st

#funciona   1º
#df_data = st.session_state["data"]
#clube = df_data["Team"].value_counts().index
#team = st.sidebar.selectbox("Clube", clube)

st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")

df_data = st.session_state["data"]
Liga = df_data["League"].value_counts().index
League = st.sidebar.selectbox("Liga", Liga)

df_clube = df_data[df_data["League"] == League]
clubes = df_clube["Team"].value_counts().index
clube = st.sidebar.selectbox("Cube", clubes)

df_players = df_data[df_data["Team"] == clube]
players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("jogador", players)

player_stats = df_data[df_data["Name"] == player].iloc[0]
#Localiza url no site EA FC25, falta adicionar .png no final, para carregar somente a imagem.
#st.image(player_stats["url"])
st.title(f"{player_stats["Name"]}")

st.markdown(f"**Liga:** {player_stats["League"]}")
st.markdown(f"**clube:** {player_stats["Team"]}")
st.markdown(f"**Posição:** {player_stats["Alternative positions"]}")
st.markdown(f"**Idade:** {player_stats["Age"]}")
st.markdown(f"**Overall:** {player_stats["OVR"]}")
st.markdown(f"**Link fonte:** {player_stats["url"]}")