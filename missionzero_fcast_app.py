import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
import joblib
import statsmodels
from PIL import Image, ImageOps

col1, mid, col2 = st.columns([1,1,20])
turbine=Image.open('green_wind.png')

with col1:
       st.image(turbine, width=65)
with col2:
        st.markdown("<h1 style='text-align: center; color: green; font-size: 38px; font-style: italic; margin-bottom: 30px; whitespace: nowrap'>Will there be enough (Wind) energy?</h1>", unsafe_allow_html=True)

#write a subheader     
#st.markdown("<h2 style='text-align: center;  font-size: 16px; margin-bottom: 30px'>Time Series Analysis on National Grid ESO Generation Data (2009 - 2024)</h2>", unsafe_allow_html=True)

#######################################################################################
#model calculations
model = joblib.load('wind_generation_SARIMA_model.pkl')

year_to_forecast = st.sidebar.selectbox('Select a year to forecast:', range(2024, 2050))

#calculate steps for model to forecast from 2023 onwards
#X3_w_test starts May 2020
steps_rem_2020 = 8
steps_2021_to_2023 = 3*12
steps_test = steps_rem_2020 + steps_2021_to_2023 + (12*(int(year_to_forecast)-2023))

#generate forecast
forecast = model.forecast(steps=steps_test)

#calculate total generation for selected year (MWh)
#data is in half-hourly records; divide by 2 to get MWh
selected_yr_forecasted_mwh = forecast.loc[str(year_to_forecast)].sum() / 2

#calculate TWh
selected_yr_forecasted_twh = selected_yr_forecasted_mwh/1000000

#load .csv of non-wind generation in 2023
non_wind_data = pd.read_csv('energy_gen_2023_excl_wind.csv')

#add wind calculations to dataframe
non_wind_data.loc[len(non_wind_data)] = ['WIND', selected_yr_forecasted_mwh]

#calculate total energy generation
total_generation = non_wind_data['Generation (MWh)'].sum()

#calculate total energy opex
total_cost = selected_yr_forecasted_mwh*176
total_cost_bil = total_cost/1000000000

############################################################################
#DOUGHNUT CHART

#create doughnut plot
colors_dict = {'GAS': 'firebrick', 'NUCLEAR': 'greenyellow', 'IMPORTS':'turquoise', 'BIOMASS': 'darkviolet', 'SOLAR': 'gold', 'HYDRO': 'lightseagreen', 'COAL': 'dimgray',   
        'STORAGE': 'salmon', 'WIND': 'royalblue'}

values = non_wind_data['Generation (MWh)'].tolist()
labels = non_wind_data['Energy Sources'].tolist()
colors = [colors_dict.get(label, 'default_color') for label in labels]

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, 
                            pull=[0, 0, 0, 0, 0, 0, 0, 0, 0], 
                            marker_colors=colors, 
                            textinfo='label',
                            outsidetextfont=dict(color='black'),
                            hoverinfo='percent',
                            hoverlabel=dict(font=dict(size=16, color='black')),
                            showlegend=False)])

fig.update_layout(title={'text': f'UK Energy Mix in {year_to_forecast} <br><span style="font-size: 16px; font-style: italic;"> (select a year on left panel to forecast opex and TWh)</span>', 
                        'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font_size': 30}, uniformtext_minsize=15, uniformtext_mode='hide', 
                        annotations=[
                            dict(text=f'Wind OpEx <br>', x=0.5, y=0.62, font=dict(size=22, color='black'), showarrow=False), 
                            dict(text=f'<b>£{round(total_cost_bil,0)} bil<b> <br>', x=0.5, y=0.5, font=dict(size=45, color='black'), showarrow=False), 
                            dict(text=f'{round(selected_yr_forecasted_twh,0)} TWh', x=0.5, y=0.38, font=dict(size=30, color='black'), showarrow=False, 
                            textangle=0, align='center')], width=750, height=750,
                            margin=dict(t=125, b=75, l=0, r=0))

fig.update_traces(textfont=dict(size=16))

#display doughnut chart in Streamlit

st.plotly_chart(fig, use_container_width=True)

############################################################################
#write a subheader     
st.markdown("<h4 style='text-align: left;  font-size: 12px; color: gray; font-style: italic; margin-bottom: 30px'>(assuming static 2023 generation for non-wind energy sources)</h2>", unsafe_allow_html=True)

############################################################################

years_into_the_future = year_to_forecast - 2023
st.markdown(f"Wind energy generation forecasted <span style='font-weight:bold; font-size:40px;'>{years_into_the_future}</span> year(s) into the future. Annual energy generation will require:", unsafe_allow_html=True)

############################################################################

#opex and capex calculations for each energy source
w_strike_price = 176 #per MWh
w_years_to_build = 0.5
cost_wind_farm = 617.38 #mil GBP per 50-turbine farm, 2.75MW ea
w_mwh_year = 219000 #50 turbines * 4380MWh/yr per turbine

w_total_opex = w_strike_price * selected_yr_forecasted_mwh 
w_total_capex = (years_into_the_future/w_years_to_build)* cost_wind_farm
w_total_cost = (w_total_opex + w_total_capex)/1000000000
w_total_farms = selected_yr_forecasted_mwh/w_mwh_year



s_strike_price = 61 #per MWh
s_years_to_build = 1
s_mwh_year = 42 #20MW farm * 2.1 MWH/year/MW
cost_solar_farm = 0.98 #mil GBP per 20MW farm

s_total_opex = s_strike_price * s_mwh_year 
s_total_capex = (years_into_the_future/s_years_to_build)* cost_solar_farm
s_total_cost = (s_total_opex + s_total_capex)/100
s_total_farms = selected_yr_forecasted_mwh/s_mwh_year



n_strike_price = 87 #per MWh
n_years_to_build = 12
n_mwh_year = 25600000 #3.2GW plant * 8,000,000 MWh/year/GW
cost_nuclear_plant = 35000 #mil GBP per plant
n_total_plant = selected_yr_forecasted_mwh/n_mwh_year

n_total_opex = n_strike_price * n_mwh_year 
n_total_capex = (years_into_the_future/n_years_to_build)* cost_nuclear_plant
n_total_cost = (n_total_opex + n_total_capex)/10000000

#wind equivalent
wind_turbine = Image.open('wind_turbine_black.jpeg')

col1, col2, col3 = st.columns([1,8,2])
with col1:
    st.image(wind_turbine, width=100)
with col2:
    st.markdown(f"<div style='text-align: center; font-size: 36px; vertical-align: bottom;'><span style='font-weight:bold;'>£{int(round(w_total_cost,0))}</span> billion | <span style='font-weight: bold;'>{int(round(w_total_farms,0))}</span> wind farms</div>", unsafe_allow_html=True)


st.markdown(f"This amount of Wind energy generation equates to:", unsafe_allow_html=True)

#solar equivalent
solar = Image.open('solar_farm.png')
col1, col2, col3 = st.columns([2,14,1])
with col1:
    st.image(solar, width=125)
with col2:
    st.markdown(f"<div style='text-align: center; font-size: 36px; vertical-align: bottom;'><span style='font-weight:bold;'>£{int(round(s_total_cost,0))}</span> million | <span style='font-weight: bold;'>{int(round(s_total_farms,0))}</span> solar farms</div>", unsafe_allow_html=True)

st.markdown(f"OR:", unsafe_allow_html=True)

#nuclear equivalent
nuclear = Image.open('nuclear_plant.jpeg')
col1, col2, col3 = st.columns([1,8,1])
with col1:
    st.image(nuclear, width=100)
with col2:
    st.markdown(f"<div style='text-align: center; font-size: 36px; vertical-align: bottom;'><span style='font-weight:bold;'>£{int(round(n_total_cost,0))}</span> billion | <span style='font-weight: bold;'>{int(round(n_total_plant,0))}</span> nuclear plants</div>", unsafe_allow_html=True)