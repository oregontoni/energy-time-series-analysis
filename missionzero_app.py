import streamlit as st
from PIL import Image

from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
#numbers[#rows, #col, size]
logo = Image.open('netzerouk.png')

st.image(logo, width= 800, use_column_width='True')

st.markdown("<h1 style='color:green;'>MISSION ZERO<h1/>", unsafe_allow_html=True)


# Specify what pages should be shown in the sidebar, and what their titles 
# and icons should be
show_pages(
    [
        Page("missionzero_app.py", "Introduction", "🇬🇧"),
        Page("missionzero_fcast_app.py", "UK Net Zero 2050", "🌏"),
        Page("missionzero_btm_app.py", "Connecting", "🔗")
    ]
)

st.write(
"""
Welcome to my project on time series forecasting to predict the UK's electricity generation capacity 
and energy mix in 2050 (ie, the year the UK is legally bound to have reached NetZero). 

In 2019, the UK became the first country in the world to legally bind itself to a Net Zero target: by 2050, the UK would 
no longer add more greenhouse gases to the atmosphere than it removes.

At the end of 2023, fossil fuels were 1/3 of the UK's energy mix. 

What is the UK's current renewable energy generation capacity, and how can the UK government plan capacity growth of 
the various renewable energy sources in order to achieve NetZero while meeting energy demands?

Energy generated is an inherent reflection of energy demand. When the demand for electricity is greater than the base load 
(ie, the minimum amount of energy needed to be supplied to the grid at any given point in time), 
the National Grid reacts by providing additional electricity. National Grid ESO's data portal includes historic energy generation from 2009 to 2024, 
with data recorded in half-hour increments. 

Through time series analysis, historical data can be used to predict future values of energy output. Those outputs can then be summarised into actionable insights. 
Ultimately, insights from forecasting models can become the tools for policy makers to make decisions on how the UK can balance energy generation growth to fulfil its Net Zero obligations. 

This project is my attempt to apply the data analysis skills learned during the intensive data science bootcamp at BrainStation and 
gain a better understanding of what the UK's future energy scenario might look like.

Given the energy generation dataset is a reflection of energy demand in the UK, I used several forecasting models to conduct time series analysis and predict future values of energy output:

- Linear Regression

- XGBoost

- SARIMA and SARIMAX


"""
)
#intro
#energy mix