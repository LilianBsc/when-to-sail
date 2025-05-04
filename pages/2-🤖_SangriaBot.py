"""
Here you will find an AI agent dedicated to the Sangria boat.
"""
import streamlit as st

st.set_page_config(
    page_title="Ask SangriaBot",
    layout="wide",
    page_icon="🤖"
)

st.title("Ask SangriaBot")
st.components.v1.iframe("https://demo.ragflow.io/", height=800, scrolling=True)
