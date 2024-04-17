import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
import joblib
import statsmodels


st.markdown("<h1 style='text-align: center; color: green; font-style: italic; margin-bottom: 30px'>UK Net Zero 2050: Will there be enough renewable energy?</h1>", unsafe_allow_html=True)

#write a subheader     
st.markdown("<h2 style='text-align: center;  font-size: 16px; margin-bottom: 30px'>Time Series Analysis on National Grid ESO Generation Data (2009 - 2024)</h2>", unsafe_allow_html=True)

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

fig.update_layout(title={'text': f'UK Energy Mix in {year_to_forecast} <br><span style="font-size: 18px; font-style: italic;"> (assuming static 2023 generation for non-wind energy sources)</span>', 
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
