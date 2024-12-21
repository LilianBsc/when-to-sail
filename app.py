import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Configurer Streamlit en mode pleine largeur
st.set_page_config(layout="wide")

df = pd.read_csv("/home/hke/Desktop/projects/boat/when-to-sail/data/marees-2025.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

# Extraire les coefficients (PM1 et PM2) depuis la colonne "coefs"
df["coef PM1"] = df["coefs"].apply(lambda x: eval(x)[0])  # Premier coefficient
df["coef PM2"] = df["coefs"].apply(lambda x: eval(x)[1] if len(eval(x)) > 1 else None)  # Deuxième coefficient ou None

# Créer une nouvelle DataFrame pour les PM, en séparant chaque PM
coefs_rows = []
for i, row in df.iterrows():
    date = row["datetime"]
    coefs = eval(row["coefs"])
    pm_hours = eval(row["h PM"])
    # Pour chaque heure de PM, ajouter une ligne
    for hour, coef in zip(pm_hours, coefs):
        # Créer une ligne avec datetime et coefficient
        coefs_rows.append({
            "datetime": pd.to_datetime(f"{date.date()} {hour}"),
            "coefficient": coef
        })

# Créer la DataFrame des PM
df_pm = pd.DataFrame(coefs_rows)
# Convertir la date en format souhaité pour le hover (lundi 1 février 2025)
df_pm['formatted_date'] = df_pm['datetime'].dt.strftime('%A %d %B %Y')
# Convertir l'heure en format souhaité (07:15)
df_pm['formatted_time'] = df_pm['datetime'].dt.strftime('%H:%M')



# Titre de l'application
st.title("Marées à Binic")

# Graphique interactif avec Plotly
fig = px.line(
    df_pm,
    x="datetime",
    y="coefficient",
    markers=True,
    title="Coefficients et porte du port"
)

# Ajouter des infobulles pour afficher la date et le coefficient
fig.update_traces(
    hovertemplate="<b>Date</b>: %{customdata[0]}<br><b>Heure PM</b>: %{customdata[1]}<br><b>Coefficient</b>: %{y}<extra></extra>",
    customdata=df_pm[["formatted_date", "formatted_time"]].values
)

# Affichage des boutons pour contrôler l'affichage des formes
display_seuil = st.checkbox("Afficher le seuil", value=False)
display_weekends = st.checkbox("Afficher les week-ends", value=False)

if display_seuil:
    # Ajouter une ligne horizontale à coefs = 45
    fig.add_hline(
        y=45,
        line_dash="dash",
        line_color="red",
    )

    # Ajouter une zone colorée sous la ligne
    fig.add_shape(
        type="rect",
        x0=df["datetime"].min(),  # Début de la zone (première date)
        x1=df["datetime"].max(),  # Fin de la zone (dernière date)
        y0=0,  # Début de la zone (coefficient min)
        y1=45,  # Fin de la zone (seuil de 45)
        fillcolor="rgba(255, 0, 0, 0.3)",  # Couleur rouge avec transparence (0.3)
        line=dict(color="red", width=0),  # Pas de bordure
        opacity=0.3,  # Transparence de la zone
    )


    # Ajouter une annotation explicite pour la légende de la zone
    fig.add_annotation(
        x=df["datetime"].median(),  # Position horizontale sur la dernière date
        y=45,  # Position verticale au niveau du seuil
        text="Seuil de fermeture des portes = 45",  # Texte à afficher
        showarrow=True,  # Afficher une flèche pointant vers le seuil
        arrowhead=2,  # Style de la flèche
        arrowsize=1,  # Taille de la flèche
        ax=0,  # Décalage horizontal de la flèche
        ay=80,  # Décalage vertical de la flèche
        font=dict(size=12),  # Police du texte
        align="center"  # Alignement du texte
    )

if display_weekends:
    # Ajouter des barres verticales vertes aux week-ends
    samedis = df[df["date"].str.startswith(("samedi"))]   # Filtrer les week-ends

    print(samedis["datetime"])
        # Ajouter une ligne verticale pour chaque week-end
    for i in range(len(samedis)):
        start_date = samedis.iloc[i]["datetime"]
        end_date = start_date + + pd.Timedelta(days=2)
        
        # Ajouter la forme pour le week-end
        fig.add_shape(
            type="rect",
            x0=start_date,  # Début du week-end
            x1=end_date,  # Fin du week-end
            y0=0,  # Début de la zone (coefficient min)
            y1=120,  # Fin de la zone (valeur max du coefficient)
            fillcolor="rgba(0, 255, 60, 0.576)",  # Couleur verte avec transparence
            line=dict(color="green", width=0),  # Pas de bordure
            opacity=0.3,  # Transparence de la zone
        )

# Afficher le graphique dans Streamlit
st.plotly_chart(fig, use_container_width=True)