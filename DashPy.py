import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("Vendas -DashPy.csv", sep=",")
df["MES"] = pd.to_datetime(df["MES"])
df=df.sort_values("MES")

df["Month"] = df["MES"].apply(lambda x: str(x.year) + "-" +str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())