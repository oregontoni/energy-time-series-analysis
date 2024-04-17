import streamlit as st
from PIL import Image, ImageOps

chart_logo = 'green_chart_line.png'
energy_over_time = 'energy_generation_2009_to_2023.png'
energy_comparison = 'energy_gen_2009v2023.png'
energy_month = 'generation_by_month_09to24.png'
energy_neg_gen = 'y_train_fitx_matching.png'
energy_wind_fcst = 'y_train_fw3_forecasted2049.png'

col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image(chart_logo, width=80)
with col2:
    st.markdown("<h1 style='text-align: left; font-size: 30px; color: green; font-style: italic; margin-bottom: 30px; whitespace: nowrap'>Before forecasting.....what are the trends?</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: left; font-size: 16px; color: black; margin-bottom: 1px; whitespace: nowrap'>Micro trends: monthly</h2>", unsafe_allow_html=True)
st.markdown("""<p style='color: grey;'>The monthly averages--the red horizontal lines--show a seasonal energy generation pattern through the years. The highest points are in winter and the lowest points are in summer.
</p>""", unsafe_allow_html=True)
photo = st.container(border=False)
photo.image(energy_month, width=700)

st.markdown("<h2 style='text-align: left; font-size: 16px; color: black; margin-bottom: 1px; whitespace: nowrap'>Macro trends: all 15 years of data</h2>", unsafe_allow_html=True)
st.markdown("""<p style='color: grey;'>There is a general downward trend in energy generation over the 15 years. Coal has declined to almost zero during the UK's transition away from fossil fuels.
</p>""", unsafe_allow_html=True)
photo = st.container(border=False)
photo.image(energy_over_time, width=700)

st.markdown("<h2 style='text-align: left; font-size: 16px; color: black; margin-bottom: 1px; whitespace: nowrap'>How will the general downward trend in energy generation translate into forecast modelling.........?</h2>", unsafe_allow_html=True)
photo = st.container(border=False)
photo.image(energy_neg_gen, width=700)

st.markdown("<h2 style='text-align: left; font-size: 16px; color: black; margin-bottom: 1px; whitespace: nowrap'>..............will the UK realistically be generating negative levels of energy in 2050?</h2>", unsafe_allow_html=True)
st.markdown("""<p style='color: grey;'>Although there was an overall downward slope the historical trends graph, not all energy sources have declined in total energy output since 2009. In contrast to declining Coal energy generation, Wind energy generation has grown exponentially.
</p>""", unsafe_allow_html=True)
photo = st.container(border=False)
photo.image(energy_comparison, width=700)

#with st.sidebar.container():
#    turbine = Image.open('wind_tbin_drwg.png')
#    st.image(turbine, width= use_column_width=True)
