import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

import plotly.express as px
import pandas as pd
import streamlit as st

def created_coefs_df(df: pd.DataFrame):
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
    df_coefs = pd.DataFrame(coefs_rows)
    # Convertir la date en format souhaité pour le hover (lundi 1 février 2025)
    df_coefs['formatted_date'] = df_coefs['datetime'].dt.strftime('%A %d %B %Y')
    # Convertir l'heure en format souhaité (07:15)
    df_coefs['formatted_time'] = df_coefs['datetime'].dt.strftime('%H:%M')

    return df_coefs

def color_weekends(fig, start_date, end_date, y0=0, y1=120, fillcolor="rgba(0, 255, 60, 0.576)", opacity=0.3):
    """
    Ajoute des barres vertes sur les week-ends pour une plage de dates donnée dans une figure Plotly.

    Arguments :
    - fig : objet Plotly figure où les week-ends seront ajoutés.
    - start_date : début de la période (format "YYYY-MM-DD").
    - end_date : fin de la période (format "YYYY-MM-DD").
    - y0 : valeur minimale de l'axe y pour le rectangle.
    - y1 : valeur maximale de l'axe y pour le rectangle.
    - fillcolor : couleur de remplissage des rectangles (par défaut vert transparent).
    - opacity : opacité des rectangles (0 = transparent, 1 = opaque).
    """
    # Conversion des dates en objets datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Générer toutes les dates entre start_date et end_date
    all_dates = pd.date_range(start=start_date, end=end_date)

    # Filtrer les week-ends (samedi et dimanche)
    weekends = all_dates[all_dates.weekday >= 5]

    # Ajouter un rectangle pour chaque week-end
    for weekend in weekends:
        fig.add_shape(
            type="rect",
            x0=weekend,
            x1=weekend + pd.Timedelta(days=1),  # Fin du week-end (dimanche)
            y0=y0,
            y1=y1,
            fillcolor=fillcolor,
            line=dict(color="green", width=0),  # Pas de bordure
            opacity=opacity
        )

def display_coefs_chart(df_coefs: pd.DataFrame):
    # Graphique interactif avec Plotly
    fig = px.line(
        df_coefs,
        x="datetime",
        y="coefficient",
        markers=True,
        title="Coefficients et porte du port"
    )

    # Ajouter des infobulles pour afficher la date et le coefficient
    fig.update_traces(
        hovertemplate="<b>Date</b>: %{customdata[0]}<br><b>Heure PM</b>: %{customdata[1]}<br><b>Coefficient</b>: %{y}<extra></extra>",
        customdata=df_coefs[["formatted_date", "formatted_time"]].values
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
            x0=df_coefs["datetime"].min(),  # Début de la zone (première date)
            x1=df_coefs["datetime"].max(),  # Fin de la zone (dernière date)
            y0=0,  # Début de la zone (coefficient min)
            y1=45,  # Fin de la zone (seuil de 45)
            fillcolor="rgba(255, 0, 0, 0.3)",  # Couleur rouge avec transparence (0.3)
            line=dict(color="red", width=0),  # Pas de bordure
            opacity=0.3,  # Transparence de la zone
        )


        # Ajouter une annotation explicite pour la légende de la zone
        fig.add_annotation(
            x=df_coefs["datetime"].median(),  # Position horizontale sur la dernière date
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
        color_weekends(
            fig,
            start_date=df_coefs["datetime"].min(),
            end_date=df_coefs["datetime"].max(),
            y0=0,
            y1=120,
            fillcolor="rgba(0, 255, 60, 0.576)",
            opacity=0.3
            )
    
    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)