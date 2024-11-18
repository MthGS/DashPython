import streamlit as st

st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")

df_data = st.session_state["data"]
clube = df_data["Team"].value_counts().index
team = st.sidebar.selectbox("Clube", clube)

team_stats = df_data[df_data["Team"] == team].iloc[0]
#Localiza url no site EA FC25, falta adicionar .png no final, para carregar somente a imagem.
#st.image(player_stats["url"])
st.title(f"{team_stats["Team"]}")

st.markdown(f"**League:** {team_stats["League"]}")