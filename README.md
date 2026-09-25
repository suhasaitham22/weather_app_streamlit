# Weather App (Streamlit)

A simple weather app built with Streamlit and the OpenWeatherMap API. Enter a city name to see the current weather, and pick a start date to explore historical temperature data with charts.

## What it does

`pro2.py` has two main features:

1. **Current weather** — `getweather()` calls the OpenWeatherMap current weather endpoint and shows the city, country, temperature (C), feels-like temperature, humidity, description, and weather icon.
2. **Historical data** — `historical_data()` calls the One Call timemachine endpoint for the city's coordinates and the selected date, then shows the hourly temperatures as a Streamlit line chart plus Plotly box plot and histogram.

Unknown cities show a "City not found!" error.

## Install and run

You need a free [OpenWeatherMap](https://openweathermap.org/api) API key.

```bash
git clone https://github.com/suhasaitham22/weather_app_streamlit.git
cd weather_app_streamlit
pip install -r requirements.txt
```

Add your key to `.streamlit/secrets.toml` (the app reads `st.secrets["api_key"]`):

```toml
api_key = "your_openweathermap_key"
```

Then:

```bash
streamlit run pro2.py
```

## Tech stack

Streamlit, requests, pandas, Plotly, OpenWeatherMap API.
