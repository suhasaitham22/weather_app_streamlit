# Modules
import streamlit as st
import requests
from datetime import datetime , timedelta
import pandas as pd

# INSERT YOUR API  KEY WHICH YOU PASTED IN YOUR secrets.toml file 
api_key =  st.secrets["api_key"]

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_1 = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}'

# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url.format(city, api_key))     
    if result:
        json = result.json()
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1),round(temp_feels,1),
                humid,lon,lat,icon,des]
        return res , json
    else:
        print("error in search !")

# Function for HISTORICAL DATA
def get_hist_data(lat,lon,start):
    res = requests.get(url_1.format(lat,lon,start,api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)     
    return data , temp

# Define app title and description
st.set_page_config(page_title='Weather App', page_icon=':partly_sunny:', layout='wide')
st.title('Weather App')
st.markdown('This is a simple weather app that allows you to get the latest weather data and historical data for the past 5 days for any city in the world.')

# Add an image
st.image('image.jpg', use_column_width=True)

# Create two columns
col1, col2 = st.beta_columns(2)

# Create a text input for city name in column 1
with col1:
    city_name = st.text_input("Enter a city name")

# Display current weather data and an image in column 2
with col2:  
    if city_name:
        res , json = getweather(city_name)
        st.success('Current Temperature: ' + str(round(res[1],2)) + '°C')
        st.info('Feels Like: ' + str(round(res[2],2)) + '°C')
        st.subheader('Status: ' + res[7])
        web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+str(res[6])+"@2x.png)"
        st.markdown(web_str)  

# Create an expander to display historical data for the past 5 days
if city_name:        
    show_hist = st.beta_expander(label = 'Last 5 Days History')
    with show_hist:
        start_date_string = st.date_input('Select a date')
        date_df = []
        max_temp_df = []
        for i in range(5):
            date_Str = start_date_string - timedelta(i)
            start_date = datetime.strptime(str(date_Str),"%Y-%m-%d")
            timestamp_1 = datetime.timestamp(start_date)
            his , temp = get_hist_data(res[5],res[4],int(timestamp_1))
            date_df.append(date_Str)
            max_temp_df.append(max(temp) - 273.5)
        
        # Create a table to display historical data
        df = pd.DataFrame()
        df['Date'] = date_df
        df['Max Temperature'] = max_temp_df
        st.table(df)

# Add a map to display the location of the city
if city_name:
    res , json = getweather(city_name)
    st.map(pd.DataFrame({'Latitude' : [res[5]], 'Longitude' : [res[4]]}))

# Add some additional information and credits
st.markdown('Data provided by OpenWeatherMap API. Icon made by Freepik from www.flaticon.com')
