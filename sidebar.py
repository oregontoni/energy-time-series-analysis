import streamlit as st

def navbar():
    st.sidebar.page_link("missionzero_app.py", label="Introduction", icon="🇬🇧")
    st.sidebar.page_link("pages/missionzero_tandn_app.py", label="Then & Now", icon="⌛")
    st.sidebar.page_link("pages/missionzero_fcast_app.py", label="UK Net Zero 2050", icon="🌏")
    st.sidebar.page_link("pages/missionzero_btm_app.py", label="Connecting", icon="🔗")