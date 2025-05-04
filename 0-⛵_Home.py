"""
The home page of the app.
"""
import streamlit as st
from datetime import date

# Définir le layout global
st.set_page_config(
    page_title="Bienvenue à bord de Jimbo 🌊",
    layout="centered",
    page_icon="⛵"
)

# Style personnalisé (fond clair bleu pastel, police douce)
st.markdown(
    """
    <style>
    body {
        background-color: #f0f9ff;
    }
    .title {
        font-size: 2.5em;
        font-weight: 700;
        color: #045c75;
        text-align: center;
    }
    .subtitle {
        font-size: 1.2em;
        color: #06606d;
        text-align: center;
    }
    .section {
        padding: 1em;
        border-radius: 0.5em;
        background-color: #ffffffcc;
        margin-bottom: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre principal
st.markdown('<div class="title">🧭 Bienvenue à bord de Jimbo ⛵</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Planifiez vos navigations depuis Binic, entre marées, seuils et horizons 🌅</div>', unsafe_allow_html=True)

st.markdown("")

# Présentation de l'application
with st.container():
    st.markdown("### 🌊 À propos de l'application")
    st.markdown(
        """
        Cette application est conçue pour faciliter la planification des navigations à bord de **Jimbo**, 
        un voilier Sangria basé au port de **Binic**.

        Elle vous permet de :
        - 🔄 **Consulter les horaires de marées, coefficients et seuils** du port.
        - 🚌 **Voir les horaires de bus** pour organiser votre retour ou départ.
        - 📆 **Identifier les week-ends propices à la sortie** en mer.
        - 🤖 **Discuter avec un agent intelligent** spécialisé dans le modèle *Sangria*, pour toute question technique ou pratique.

        L'objectif : **naviguer sereinement, au bon moment, avec les bonnes infos**.
        """
    )

st.divider()

# Accès aux fonctionnalités
st.markdown("### 🚪 Pages principales")
st.page_link("pages/1-📍_Infos_Binic.py", label="Infos Binic", icon="📍")
st.page_link("pages/2-🤖_SangriaBot.py", label="SangriaBot", icon="🤖")

st.markdown("---")
st.caption(f"Version du {date.today().strftime('%d/%m/%Y')} — Bon vent ! 🌬️")

