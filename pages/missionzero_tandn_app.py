import streamlit as st
from PIL import Image, ImageOps
from sidebar import navbar

def main():

    navbar()

    chart_logo = './streamlit_images/green_chart_line.png'
    energy_over_time = './figures/energy_generation_2009_2023.png'
    energy_comparison = './figures/energy_compare_2009v2023_wind.png'
    energy_month = './figures/generation_by_month_09to24.png'
    energy_neg_gen = './figures/y_train_fitx_matching.png'
    energy_wind_fcst = './figures/y_train_fw3_forecasted2049.png'

    col1, mid, col2 = st.columns([1,1,20])
    with col1:
        st.image(chart_logo, width=80)
    with col2:
        st.markdown("<h1 style='text-align: left; font-size: 34px; color: green; font-style: italic; margin-bottom: 30px; whitespace: nowrap'>Before forecasting.....what are the trends?</h1>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: left; font-size: 20px; color: black; margin-bottom: 1px; whitespace: nowrap'>\"Always EDA. Always.\"</h2>", unsafe_allow_html=True)
    st.markdown("""<p style='color: grey; font-size: 15px;'>Simply put, EDA (Exploratory Data Analysis) is asking the question: what general patterns can be seen in the data? Before applying any manipulation, what context can these patterns provide to our further research?
    </p>""", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: left; font-size: 20px; color: black; margin-bottom: 1px; whitespace: nowrap'>Micro trends: monthly</h2>", unsafe_allow_html=True)
    st.markdown("""<p style='color: grey; font-size: 15px;'>The monthly averages--the red horizontal lines--show a U-pattern. This shows a seasonal energy generation pattern, with the highest points in winter and the lowest points in summer.
    </p>""", unsafe_allow_html=True)
    photo = st.container(border=False)
    photo.image(energy_month, width=700)

    st.markdown("<h2 style='text-align: left; font-size: 20px; color: black; margin-bottom: 1px; whitespace: nowrap'>Macro trends: all 15 years of data</h2>", unsafe_allow_html=True)
    st.markdown("""<p style='color: grey;'>There is a general downward trend in energy generation over the 15 years. Coal has declined to almost zero during the UK's transition away from fossil fuels.
    </p>""", unsafe_allow_html=True)
    photo = st.container(border=False)
    photo.image(energy_over_time, width=700)

    st.markdown("<h2 style='text-align: left; font-size: 20px; color: black; margin-bottom: 1px; whitespace: nowrap'>How will the general downward trend in energy generation translate into forecast modelling?</h2>", unsafe_allow_html=True)
    st.markdown("""<p style='color: grey; font-size: 15px;'>Unfortunately, the downward trend seen in EDA presented a limitation to the model's ability to accurately forecast future values. (The UK total generation being negative in 2050 is a highly unlikely future scenario.)
    </p>""", unsafe_allow_html=True)
    photo = st.container(border=False)
    photo.image(energy_neg_gen, width=700)

    st.markdown("<h2 style='text-align: left; font-size: 20px; color: black; margin-bottom: 1px; whitespace: nowrap'>How can we model a more realistic scenario for UK energy generation in 2050?</h2>", unsafe_allow_html=True)
    st.markdown("""<p style='color: grey; font-size: 15px;'>Although there was an overall downward slope the historical trends graph, not all energy sources have declined in total energy output since 2009. Compared to other renewable energy sources, total Wind energy generation (in blue) has grown significantly from 2009 to 2023.
    </p>""", unsafe_allow_html=True)
    photo = st.container(border=False)
    photo.image(energy_comparison, width=700)

    st.markdown("<h2 style='text-align: left; font-size: 20px; color: black; margin-bottom: 1px; whitespace: nowrap'>Is Wind the future of UK renewable energy?</h2>", unsafe_allow_html=True)
    st.markdown("""<p style='color: grey; font-size: 15px;'>The same SARIMA model used to predict overall generation predicts positive total energy generation when modelling solely for wind generation.
    </p>""", unsafe_allow_html=True)
    photo = st.container(border=False)
    photo.image(energy_wind_fcst, width=700)

    st.markdown("""<p style='color: grey; font-size: 15px;'>Next, we will compare the modelled wind energy generation capacity growth alongside static energy capacity for other energy sources.
    </p>""", unsafe_allow_html=True)

if __name__ == '__main__':
    main()