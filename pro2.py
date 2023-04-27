# Modules
import streamlit as st
import requests
from datetime import datetime , timedelta
import pandas as pd
import plotly.graph_objects as go

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
        humid = json['main']['humidity']
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

# Function to display latest weather data
def latest_weather(city):
    res, json_data = getweather(city)
    country, temp, temp_feels, humid, lon, lat, icon, des = res
    st.write(f"**Current Weather in {city.title()}, {country}**")
    st.write(f"**Temperature:** {temp}°C")
    st.write(f"**Feels Like:** {temp_feels}°C")
    st.write(f"**Humidity:** {humid}%")
    st.write(f"**Description:** {des.title()}")
    st.image(f"http://openweathermap.org/img/wn/{icon}.png")

# Function to display historical data
def historical_data(city, start_date):
    res, temp = get_hist_data(city["lat"], city["lon"], int(datetime.timestamp(start_date)))
    df = pd.DataFrame(temp, columns=["Temperature"])
    df.index = pd.to_datetime([datetime.utcfromtimestamp(res["hourly"][i]["dt"]) for i in range(len(res["hourly"]))])
    st.write(f"**Historical Temperature Data for {city['name'].title()}**")
    st.line_chart(df)

    # Create a box plot of the temperature data
    fig = go.Figure()
    fig.add_trace(go.Box(y=df["Temperature"], name="Temperature"))
    fig.update_layout(title="Temperature Box Plot", xaxis_title="Temperature (°C)")
    st.plotly_chart(fig)

    # Create a histogram of the temperature data
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df["Temperature"], nbinsx=20, name="Temperature"))
    fig.update_layout(title="Temperature Histogram", xaxis_title="Temperature (°C)", yaxis_title="Count")
    st.plotly_chart(fig)

# Streamlit app
st.title("Weather App")
st.write("Welcome to the Weather App! With this app, you can get the latest weather data and historical temperature data for any city in the world. Simply enter the name of the city and select a start date, and the app will display the relevant data. The app also includes visualizations of the historical temperature data, so you can see how temperatures have changed over time.")
st.image("image.jpg", use_column_width=True)
city = st.text_input("Enter a city name")
start_date = st.date_input("Select a start date")

if city:
    latest_weather(city)

if city and start_date:
    res = requests.get(url.format(city, api_key))
    json_data = res.json()
    if json_data["cod"] != "404":
        city_data = {"name": json_data["name"], "lat": json_data["coord"]["lat"], "lon": json_data["coord"]["lon"]}
        historical_data(city_data, start_date)
    else:
        st.error("City not found!")
