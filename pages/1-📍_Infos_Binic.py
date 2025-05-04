"""
This is the page to decide when is the best time to go to Binic.
It includes:
- tide coefs and times
- Port gate thresholds
- weekends
"""
# TODO: Add bus infos

import streamlit as st

import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

import pandas as pd
from datetime import datetime

from services.coefs_chart import created_coefs_df, display_coefs_chart
from services.daily_data import afficher_marees

st.set_page_config(
    page_title="Infos Binic",
    page_icon="📍"
)

df = pd.read_csv("data/marees-2025.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

df_coefs = created_coefs_df(df)

# Titre de l'application
st.title("Infos Binic")

with st.container(border=True):
    display_coefs_chart(df_coefs)

with st.container(border=True):
    date_cible = st.date_input("Infos nav pour", datetime.now())
    afficher_marees(date_cible, df)
