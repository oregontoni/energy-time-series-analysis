import streamlit as st

wind_turbine = open('wind_turbine.mp4', 'rb')
video_bytes = wind_turbine.read()

#

st.video(wind_turbine, loop=True)