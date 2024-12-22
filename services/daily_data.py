import streamlit as st
import pandas as pd
from datetime import datetime

def afficher_marees(date_cible, df, n_days=1):
    # Convertir la date cible en datetime
    date_cible = pd.to_datetime(date_cible)
    
    # Filtrer les 3 jours autour de la date cible
    filtered_df = df[(df["datetime"] >= date_cible - pd.Timedelta(days=n_days)) & 
                     (df["datetime"] <= date_cible + pd.Timedelta(days=n_days))]
    row_st = st.columns(3)
    col_number = 0
    for _, row in filtered_df.iterrows():
        col = row_st[col_number]
        col_number += 1
        rows = []
        jour = row["date"]
        col.subheader(jour)

        h_PM = eval(row['h PM'])
        h_BM = eval(row['h BM'])
        hde_PM = eval(row['hde PM'])
        hde_BM = eval(row['hde BM'])
        coefs = [60, 60]

        # Ajouter les événements dans des lignes distinctes
        for i in range(len(h_PM)):
            rows.append(["PM", h_PM[i], hde_PM[i], coefs[i]])
        for i in range(len(h_BM)):
            rows.append(["BM", h_BM[i], hde_BM[i], "N/A"])

        table_df = pd.DataFrame(rows, columns=["Type", "Horaire", "Hauteur", "Coefficient"])
        table_df["Horaire"] = pd.to_datetime(table_df["Horaire"], format="%H:%M").dt.time
        table_df["Horaire"] = table_df["Horaire"].apply(lambda x: x.strftime("%H:%M"))
        table_df = table_df.sort_values(by="Horaire")
        col.dataframe(table_df, hide_index=True)