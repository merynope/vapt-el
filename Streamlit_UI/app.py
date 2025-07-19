import streamlit as st
import dashboard
import classifyPage

st.set_page_config(
    page_title="Ethical Hacking EL",
    page_icon="🤖",
    layout="wide")

PAGES = {
    "Dashboard": dashboard,
    "Classify Image": classifyPage
}

st.sidebar.title("Ethical Hacking Lab Part B - Experential Learning")

st.sidebar.write("Created by - Meryn, Nivedita")

st.sidebar.subheader('Navigation:')
selection = st.sidebar.radio("", list(PAGES.keys()))

page = PAGES[selection]

page.app()
