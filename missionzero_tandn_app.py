import streamlit as st
from PIL import Image, ImageOps

energy_over_time = 'energy_09to23_stacked.png'
energy_comparison = 'energy_gen_2009v2023.png'


photo = st.container(border=False)
photo.image(logo, width= 250)