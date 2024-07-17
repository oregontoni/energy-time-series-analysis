import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
import joblib
import statsmodels
from PIL import Image, ImageOps

def main():

    col1, mid, col2 = st.columns([1,1,20])
    turbine=Image.open('./streamlit_images/green_wind.png')

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
    selected_yr_forecasted_wind_mwh = forecast.loc[str(year_to_forecast)].sum() / 2

    #calculate TWh
    selected_yr_forecasted_wind_twh = selected_yr_forecasted_wind_mwh/1000000

    #load .csv of non-wind generation in 2023
    non_wind_data = pd.read_csv('./data/energy_gen_2023_excl_wind.csv')

    #add wind calculations to dataframe
    non_wind_data.loc[len(non_wind_data)] = ['WIND', selected_yr_forecasted_wind_mwh]

    #calculate total energy generation
    total_generation = non_wind_data['Generation (MWh)'].sum()

    #calculate total energy opex
    total_cost = selected_yr_forecasted_wind_mwh*67
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

    fig.update_layout(title={'text': f'UK Energy Mix in {year_to_forecast} <br><span style="font-size: 16px; font-style: italic;"> (select a year on left panel to forecast TWh)</span>', 
                            'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font_size': 30}, uniformtext_minsize=15, uniformtext_mode='hide', 
                            annotations=[
                                dict(text=f'<b>{round(selected_yr_forecasted_wind_twh,0)} TWh<b> <br>', x=0.5, y=0.5, font=dict(size=45, color='black'), showarrow=False),
                                dict(text=f'wind generation', x=0.5, y=0.41, font=dict(size=28, color='black'), showarrow=False,
                                textangle=0, align='center')], width=750, height=750,
                                margin=dict(t=125, b=75, l=0, r=0))

    fig.update_traces(textfont=dict(size=16))

    #display doughnut chart in Streamlit

    st.plotly_chart(fig, use_container_width=True)

    ############################################################################
    #write a subheader     
    st.markdown("<h4 style='text-align: left;  font-size: 15px; color: gray; font-style: italic; margin-bottom: 30px'>(assuming static 2023 generation for non-wind energy sources)</h2>", unsafe_allow_html=True)

    ############################################################################

    st.markdown("""<p style='color: black; font-size: 25px;'>UK energy demand in 2050 is estimated to be <span style='font-weight:bold;'>610 TWh</span>. <p style='color: grey; font-size: 15px; font-style: italic; margin-bottom: 30px'>How will energy generation forecasts affect UK policy makers' decisions for infrastructure growth?
    </p>""", unsafe_allow_html=True)
    ############################################################################

    years_into_the_future = year_to_forecast - 2023
    st.markdown(f"Wind energy generation forecasted <span style='font-weight:bold; font-size:40px;'>{years_into_the_future}</span> year(s) into the future. Annual energy generation will require:", unsafe_allow_html=True)

    ############################################################################

    #opex and capex calculations for each energy source

    #WIND
    #UK govt March 2024 strike prices for onshore and offshore wind
    w_off_strike_price = 73 #per MWh
    w_on_strike_price = 64 #per MWh
    w_years_to_build = 0.5

    #avg build cost per 50-turbine farm
    cost_wind_farm = 617380000 #mil GBP per 50-turbine farm, 2.75MW ea

    #wind generation per farm = avg 50 turbines * 4380MWh/yr per turbine
    w_mwh_year = 219000 

    w_total_farms = selected_yr_forecasted_wind_mwh/w_mwh_year
    w_total_capex = w_total_farms * cost_wind_farm
    w_total_opex = (w_off_strike_price * selected_yr_forecasted_wind_mwh * 0.66) + (w_on_strike_price * selected_yr_forecasted_wind_mwh * 0.33)
    w_total_cost = (w_total_capex + w_total_opex)/1000000000


    #SOLAR
    s_strike_price = 61 #per MWh
    s_years_to_build = 1

    #avg build cost per solar farm
    cost_solar_farm = 980000 #mil GBP per 20MW farm

    #solar generation per farm = 20MW farm * 2146 MWH/year/MW
    s_mwh_year = 42920

    s_total_farms = selected_yr_forecasted_wind_mwh/s_mwh_year
    s_total_capex = s_total_farms * cost_solar_farm
    s_total_opex = s_strike_price * selected_yr_forecasted_wind_mwh 
    s_total_cost = (s_total_capex + s_total_opex)/1000000000


    #HYDRO
    hy_strike_price = 102 #per MWh
    hy_years_to_build = 3

    cost_hydro_plant = 3400000 #mil GBP per plant

    #hydro generation per plant = 1GW plant * 4,000 MWh/year/GW
    hy_mwh_year = 4000

    hy_total_plant = selected_yr_forecasted_wind_mwh/hy_mwh_year
    hy_total_capex = hy_total_plant * cost_hydro_plant
    hy_total_opex = hy_strike_price * selected_yr_forecasted_wind_mwh
    hy_total_cost = (hy_total_capex + hy_total_opex)/1000000000


    #NUCLEAR
    n_strike_price = 87 #per MWh
    n_years_to_build = 12

    #avg build cost per nuclear power plant
    cost_nuclear_plant = 35000000000 #mil GBP per plant

    #nuclear energy generation per 3.2FW plant * 8,000,000 MWh/year/GW
    n_mwh_year = 25600000

    n_total_plant = selected_yr_forecasted_wind_mwh/n_mwh_year
    n_total_capex = n_total_plant * cost_nuclear_plant
    n_total_opex = n_strike_price * selected_yr_forecasted_wind_mwh
    n_total_cost = (n_total_capex + n_total_opex)/1000000000

    #wind equivalent
    wind_turbine = Image.open('./streamlit_images/wind_turbine_black.jpeg')

    col1, col2, col3 = st.columns([1,12,1])
    with col1:
        st.image(wind_turbine, width=100)
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 36px; vertical-align: bottom;'><span style='font-weight:bold;'>£{int(round(w_total_cost,0))}</span> Billion | <span style='font-weight: bold;'>{int(round(w_total_farms,0))}</span> wind farms </div>", unsafe_allow_html=True) 


    st.markdown(f"This amount of Wind energy generation equates to:", unsafe_allow_html=True)

    #solar equivalent
    solar = Image.open('./streamlit_images/solar_farm.png')
    col1, col2, col3 = st.columns([2,14,1])
    with col1:
        st.image(solar, width=125)
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 36px; vertical-align: bottom;'><span style='font-weight:bold;'>£{int(round(s_total_cost,0))}</span> Billion | <span style='font-weight: bold;'>{int(round(s_total_farms,0))}</span> solar farms </div>", unsafe_allow_html=True)

    st.markdown(f"OR:", unsafe_allow_html=True)

    #hydro equivalent
    hydro = Image.open('./streamlit_images/hydro_plant.jpeg')
    col1, col2, col3 = st.columns([2,14,1])
    with col1:
        st.image(hydro, width=125)
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 36px; vertical-align: bottom;'><span style='font-weight:bold;'>£{int(round(hy_total_cost,0))}</span> Billion | <span style='font-weight: bold;'>{int(round(hy_total_plant,0))}</span> hydro plants</div>", unsafe_allow_html=True)

    st.markdown(f"OR:", unsafe_allow_html=True)

    #nuclear equivalent
    nuclear = Image.open('./streamlit_images/nuclear_plant.jpeg')
    col1, col2, col3 = st.columns([1,8,1])
    with col1:
        st.image(nuclear, width=100)
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 36px; vertical-align: bottom;'><span style='font-weight:bold;'>£{int(round(n_total_cost,0))}</span> Billion | <span style='font-weight: bold;'>{int(round(n_total_plant,0))}</span> nuclear plants<sup style='font-size:.8em;'>*</sup> </div>", unsafe_allow_html=True)


    #comment * from nuclear power plants*    
    st.markdown("<h4 style='text-align: left;  font-size: 15px; color: gray; font-style: italic; margin-bottom: 30px'>*construction of nuclear power plants require an average of 12 years; an increase in nuclear energy generation capacity would lag behind hydro, which has a construction requirement of ~3 years, and wind and solar, which have construction requirements of ~1 year</h2>", unsafe_allow_html=True)

    #############################################################################################
    st.write(
    """

    **Additional points to  consider:**  

    In order to increase generation capacity to meet the estimated 610 TWh of energy demand by 2050, the UK government will likely need to implement policies that encourage the capacity growth of multiple energy sources, rather than focusing on growing capacity of a single energy source. There are some additional considerations to growing the generation capacity of  energy sources listed above.

    **Hydro:**
    - even disregarding the environmental impacts of constructiong hydropower plants (ie, flooding), many of the most economically attractive sites for hydropower schemes in the UK [have already been used](https://www.gov.uk/guidance/harnessing-hydroelectric-power). The UK government will likely only continue to develop small-scale hydro sites.

    **Nuclear:**  
    - beyond the longer construction time required for nuclear power plants, an additional [20 to 30 years is required](https://energy.ec.europa.eu/topics/nuclear-energy/decommissioning-nuclear-facilities_en) at the end of an average nuclear power plant's 30-year lifespan to remove nuclear material and complete environmental restoration of the site.  

    **Next Steps:**  
    - applying the same SARIMA model, what is the total estimated solar energy generation in 2050?
    - what is the remaining gap between estimated energy generation and estimated energy demand? 
    - how will the UK government's [updated rule for batteries](https://www.nationalgrideso.com/document/300231/download) (ie, battery storage) affect the grid's ability to accommodate growth in energy generation?  




    **Citations**  

    [2050 Energy Demand](https://www.theccc.org.uk/wp-content/uploads/2020/12/Sector-summary-Electricity-generation.pdf)  

    Opex calculations:  
    [March 2024 UK government update: maximum renewable energy strike prices per MWh](https://www.gov.uk/government/news/boost-for-offshore-wind-as-government-raises-maximum-prices-in-renewable-energy-auction)  

    Capex calculations:  

    Wind  
    [avg generation per wind turbine](http://anemoiservices.com/industry-news/how-much-electricity-does-a-wind-turbine-produce/)  
    [avg construction cost of wind farm](https://www.briefingsforbritain.co.uk/the-costs-offshore-wind-power-blindness-and-insight/#_ftn1)  
    [avg construction time of wind farm](https://www.usgs.gov/faqs/how-many-homes-can-average-wind-turbine-power)  

    Solar  
    [avg generation per solar farm](https://www.freeingenergy.com/math/solar-pv-gwh-per-mw-power-energy-mwh-m147/)  
    [avg construction cost of solar farm](https://solarenergyuk.org/news/large-scale-solar-provides-cheapest-power-says-government-report/)  
    [avg construction time of solar farm](https://solairworld.com/how-long-does-it-take-to-build-a-solar-power-plant/?expand_article=1)

    Hydro  
    [avg generation per hydro plant](https://www.renewableenergyhub.co.uk/main/hydroelectricity-information/costs-associated-with-hydroelectricity)  
    [avg construction cost of hydro plant](https://www.renewableenergyhub.co.uk/main/hydroelectricity-information/costs-associated-with-hydroelectricity)  
    [avg construction time of hydro plant](https://renewablesfirst.co.uk/renewable-energy-technologies/hydropower/hydropower-learning-centreold/how-long-will-a-hydro-project-take/)

    Nuclear  
    [avg generation per nuclear power plant](https://www.freeingenergy.com/math/nuclear-megawatt-kilowatt-hour-per-year-m193/)  
    [avg construction cost of nuclear power plant](https://www.theguardian.com/business/2024/jan/23/hinkley-point-c-could-be-delayed-to-2031-and-cost-up-to-35bn-says-edf#:~:text=It%20said%20that%20the%20cost,had%20halted%20funding%20for%20Hinkley.)  
    [avg construction time of nuclear power plant](https://www.rigzone.com/news/uk_plans_to_build_third_new_32_gw_nuclear_plant-12-jan-2024-175360-article/)  
    



    """
    )

if __name__ == '__main__':
    main()