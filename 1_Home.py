import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import streamlit.components.v1 as components
import plotly_express as px
from PIL import Image
import plotly.graph_objects as go

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

st.markdown("""
    <style>
    .funnel-container {
        width: 100%;
        max-width: 700px;
        margin: auto;
        padding-top: 30px;
    }
    .funnel-step {
        background: linear-gradient(90deg, #1f77b4, #3fa9f5);
        color: white;
        padding: 16px;
        margin-bottom: 12px;
        border-radius: 30px;
        font-size: 18px;
        font-weight: 500;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
        text-align: left;
        display: flex;
        align-items: center;
        gap: 12px;
        transition: all 0.3s ease-in-out;
    }
    .funnel-step:hover {
        transform: scale(1.03);
        background: linear-gradient(90deg, #0d6efd, #00bfff);
    }
    .flag-icon {
        width: 32px;
        height: 20px;
        border-radius: 4px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("Top 10 jogadores por OVR (com bandeiras e posição)")

st.markdown('<div class="funnel-container">', unsafe_allow_html=True)

max_ovr = max(df_data['OVR'])

for _, row in df_data.iterrows():
    nome = row['Name']
    ovr = row['OVR']
    pais = row.get('Nation', 'Unknown')
    posicao = row.get('Position', 'N/A')
    largura = int((ovr / max_ovr) * 100)

    # Obtém a bandeira do país via flagcdn (formato: https://flagcdn.com/w40/{country_code}.png)
    # Convertendo nome do país para código ISO
    import pycountry
    try:
        country = pycountry.countries.get(name=pais)
        flag_code = country.alpha_2.lower()
        flag_url = f"https://flagcdn.com/w40/{flag_code}.png"
    except:
        flag_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/BLANK_ICON.png/40px-BLANK_ICON.png"

    st.markdown(f"""
        <div class="funnel-step" style="width: {largura}%;">
            <img class="flag-icon" src="{flag_url}" alt="{pais}">
            <span>{nome} ({posicao}) — OVR {ovr}</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
