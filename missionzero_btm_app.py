import streamlit as st
from PIL import Image, ImageOps

st.title("Toni Chan")
logo = Image.open('./streamlit_images/toni_chan_photo.jpg')
qr_code_path = './streamlit_images/qr-code.png'
linkedin_logo = './streamlit_images/linkedin_logo.png'

photo = st.container(border=False)
photo.image(logo, width= 250)

col1, mid, col2 = st.columns([1,1,9])
with col1:
    st.image(linkedin_logo, width=105)
with col2:
    st.image(qr_code_path, width=105)
