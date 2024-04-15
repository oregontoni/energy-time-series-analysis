import pandas as pd
import streamlit as st
import joblib

st.title("Kickoff - Live coding an app") 

st.markdown("<h1 style='text-align: center; color: blue;'>Our last morning kick off</h1>", unsafe_allow_html=True)

def load_data(path, num_rows):

    df = pd.read_csv(path, nrows=num_rows) #dictate number of rows passed in

    # Streamlit will only recognize 'latitude' or 'lat', 'longitude' or 'lon', as coordinates
    #ie, the column names must be named as "lat" and "lon" for it to be recognised

    df = df.rename(columns={'Start Station Latitude': 'lat', 'Start Station Longitude': 'lon'})     
    df['Start Time'] = pd.to_datetime(df['Start Time'])      # reset dtype for column
     
    return df

### B. Load first 50K rows
df = load_data("NYC_bikes_small.csv", 50000)

### C. Display the dataframe in the app
st.dataframe(df)
