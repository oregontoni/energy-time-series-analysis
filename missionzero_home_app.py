import streamlit as st

wind_turbine = open('wind_turbine.mp4', 'rb')
video_bytes = wind_turbine.read()
wind_turbine.close()

st.video(wind_turbine, loop=True)
st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)