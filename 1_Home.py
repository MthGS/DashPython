import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser

if "data" not in st.session_state:
    df_data = pd.read_csv("fc25data/all_players.csv", index_col=0)
    df_data = df_data.sort_values(by="OVR", ascending=False)
    #df_data = df_data["Rank"]
    st.session_state["data"] = df_data

st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")
st.title("FC 25 DATA")
st.write("Based on eletronic arts EA FC25 data")
#st.header("Pacote de dados do nosso amado e odiado FC 25")
st.image("https://fifauteam.com/images/fc25/generic/2.webp")

#df_data = pd.DataFrame(columns=['Rank','Name','OVR'])
df = pd.read_csv("fc25data/all_players.csv")

spectra_df = pd.read_csv("fc25data/all_players.csv")
st.write(spectra_df)

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
   "Press to Download FC25 data",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
