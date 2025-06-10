import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly_express as px
from PIL import Image
import plotly.graph_objects as go

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

if "data" not in st.session_state:
    df_data = pd.read_csv("fc25data/all_players.csv", index_col=0)
    df_data = df_data.sort_values(by="OVR", ascending=False).head(10)
    #df_data = df_data["Rank"]
    st.session_state["data"] = df_data
else:
    df_data = st.session_state["data"].head(10)

# Supondo que as colunas no seu DataFrame sejam 'Name' e 'OVR'
if 'Name' in df_data.columns and 'OVR' in df_data.columns:
    nomes_jogadores = df_data['Name'].tolist()
    overall_ratings = df_data['OVR'].tolist()

    # Lista de cores para cada etapa (de cima para baixo)
    cores_funil = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    


st.logo("https://th.bing.com/th/id/OIP.GfYS4X_NrkWCHD5bvAoPegHaAl?rs=1&pid=ImgDetMain")
st.title("FC 25 DATA")
st.write("Based on eletronic arts EA FC25 data")
#st.header("Pacote de dados do nosso amado e odiado FC 25")
#st.image("https://fifauteam.com/images/fc25/generic/2.webp")

#fig = px.line(df_data, x='OVR', y='Name', title='Evolução das Vendas')

#etapas = ["Visitantes", "Cadastro", "Compra", "Entrega"]
#valores = [1000, 800, 500, 300]

# Supondo que as colunas no seu DataFrame sejam 'Name' e 'OVR'
#if 'Name' in df_data.columns and 'OVR' in df_data.columns:
#    nomes_jogadores = df_data['Name'].tolist()
#    overall_ratings = df_data['OVR'].tolist()
#
#    # Cria o gráfico de funil com Plotly
#    fig = go.Figure(go.Funnel(
#        y = nomes_jogadores,
#        x = overall_ratings,
#        textinfo = "value",
#        marker = {'color': cores_funil},
#        connector = {'visible': True, 'line': {'color': 'lightgrey', 'width': 0.5}}, # Estiliza os conectores
#        textfont = {
#            'size': 50,
#            'color': 'black'}
#    ))
#
#    # Exibe o gráfico no Streamlit
#    st.plotly_chart(fig.update_layout(
#    margin=dict(l=50, r=50, t=50, b=50)
#))

# Funil visual com bandeira do país e posição do jogador
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

st.header("All data in CSV file")
#st.slider("O", 0, 100, (25, 75))

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

