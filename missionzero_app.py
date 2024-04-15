import pandas as pd
import streamlit as st
import joblib

st.title("Mission Zero") 

st.markdown("<h1 style='text-align: center; color: blue;'>UK Net Zero 2050: Will there be enough renewable energy?</h1>", unsafe_allow_html=True)

#write a subheader
st.subheader('Time Series Analysis on National Grid ESO Generation Data (2009 - 2024)')      


model = joblib.load('wind_generation_SARIMA_model.pkl')

year_to_forecast = st.selectbox('Select a year to forecast:', range(2024, 2050))

#calculate steps for model to forecast from 2023 onwards
#X3_w_test starts May 2020
steps_rem_2020 = 8
steps_2021_to_2023 = 3*12
steps_test = steps_rem_2020 + steps_2021_to_2023 + (12*(year_to_forecast-2023))

#generate forecast
forecast = model.forecast(steps=steps_test)

#calculate total generation for selected year (MWh)
#data is in half-hourly records; divide by 2 to get MWh
selected_yr_forecasted_mwh = forecast.loc[str(year_to_forecast)].sum() / 2

#############################################################################

#DOUGHNUT CHART

#load .csv of non-wind generation in 2023
non_wind_data = pd.read_csv('energy_gen_2023_excl_wind.csv')

#display MWh forecast for wind
st.write(f'Forecasted Total Wind Generation for {year_to_forecast}: {selected_yr_forecasted_mwh} MWh')

#add wind calculations to dataframe
non_wind_data.loc[len(non_wind_data)] = ['Wind', selected_yr_forecasted_mwh]

#calculate total energy generation
total_generation = non_wind_data['Generation (MWh)'].sum()

#calculate total energy opex
total_cost = selected_yr_forecasted_mwh*176

#create doughnut plot
fig, ax = plt.subplots()
wedges, text, autotexts = ax.pie(
    non_wind_data['Generation(MWh)'],
    labels=non_wind_data['Energy Sources'],
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops=dict(width=0.3)
)

#doughnut center
center_circle = plt.Circle((0,0), 0.70, fc='darkgreen'))
fig = plt.gcf()
fig.gca().add_artist(center_circle)

#display total cost + MWh
plt.text(0, 0, f"£{total_cost} opex \n{selected_yr_forecasted_mwh} MWh",
         ha='center', va='center', fontsize=17, color='white')
plt.title(f'UK Energy Mix')
plt.show()
                    

#display doughnut chart in Streamlit
st.pyplot(fig)


"""
st.map(df)  v

def load_data(path, num_rows):

    df = pd.read_csv(path, nrows=num_rows) #dictate number of rows passed in

    df = df.rename(columns={'Start Station Latitude': 'lat', 'Start Station Longitude': 'lon'})     
    df['Start Time'] = pd.to_datetime(df['Start Time'])      # reset dtype for column
     
    return df

### B. Load first 50K rows
df = load_data("wind_gen_model_data_feed.csv", 46)

### C. Display the dataframe in the app
st.dataframe(df)

#############################################################################################################
st.subheader("Wind generation forecast using a pretrained SARIMA model")

# A. Load the model using lib
# load model
model = joblib.load("wind_generation_SARIMA_model.pkl")

# B. Set up input field
text = st.text_input('Wind generation forecast to 2050: # of years (enter a number between 1 and 26)', '2')

# C. Use the model to predict & write result
# write code to do something with the text entered

#forecast
#expect iterable object, so wrap it as a list using[ ]
forecast = y_train_fw3.forecast(steps=[text])

#display depending on if 1 or 0, positive or negative
#if text 1:
   # st.write("Positive Review")

#else:
  #  st.write("Negative Review")

#WHAT IF prediction?
prediction = model.predict_proba([text])

#display depending on if 1 or 0, positive or negative
st.write(f"Probability of positive sentiment: {round(prediction[0][1],2)}")
"""