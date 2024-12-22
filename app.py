import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

import streamlit as st

import pandas as pd
from datetime import datetime

from services.coefs_chart import created_coefs_df, display_coefs_chart
from services.daily_data import afficher_marees

# Configurer Streamlit en mode pleine largeur
st.set_page_config(layout="wide")

df = pd.read_csv("data/marees-2025.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

df_coefs = created_coefs_df(df)

# Titre de l'application
st.title("Marées à Binic")

with st.container(border=True):
    display_coefs_chart(df_coefs)

with st.container(border=True):
    date_cible = st.date_input("Infos nav pour", datetime.now())
    afficher_marees(date_cible, df)