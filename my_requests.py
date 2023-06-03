import requests
# from dotenv import load_dotenv
import os
import json
from types import SimpleNamespace
import datetime

# load_dotenv('config.env')
# key = os.environ.get("CRYPTO_API_KEY")


# URLs
url_base = 'https://pro-api.coinmarketcap.com/'
endpoint_get_cryptos = url_base + "v1/cryptocurrency/listings/latest"

# Accuweather variables
api_key = ""
city_name = "Montevideo"
DATE = datetime.datetime.now()  # Use today's date

headers = {
    'X-CMC_PRO_API_KEY': ''
}


def get_cryptos():
    response = requests.request("GET", endpoint_get_cryptos, headers=headers)
    obj = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
    return obj.data


# Accuweather
def get_location_key():
    geoposition_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city_name}"
    response = requests.get(geoposition_url)
    data = response.json()
    return data[0]['Key']


def get_hourly_forecast(location_key):
    date_str = DATE.strftime('%Y-%m-%d')
    forecast_url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}?apikey={api_key}&details=true&metric=true&date={date_str}"
    response = requests.get(forecast_url)
    forecast_data = response.json()

    message = "<b>Temperaturas para hoy: </b>\n\n"
    for hour in forecast_data:
        time = hour['DateTime'].split('T')[1][:5]
        temperature = hour['Temperature']['Value']
        unit = hour['Temperature']['Unit']
        conditions = get_condition_icon(hour['IconPhrase'])
        message += f"{time} - {temperature} {unit}  {conditions}\n"

    return message

def get_condition_icon(icon_phrase):
    weather_icons = {
        "Sunny": "☀️",
        "Mostly Sunny": "🌤️",
        "Partly Sunny": "⛅",
        "Intermittent Clouds": "🌥️",
        "Hazy Sunshine": "🌤️",
        "Mostly Cloudy": "🌥️",
        "Cloudy": "☁️",
        "Dreary (Overcast)": "☁️",
        "Fog": "🌫️",
        "Showers": "🌦️",
        "T-Storms": "⛈",
        "Thunderstorms": "⛈",
        "Rain": "🌧️",
        "Flurries": "❄️",
        "Snow": "❄️",
        "Ice": "🌨️",
        "Sleet": "🌨️",
        "Freezing Rain": "🌨️",
        "Rain and Snow": "🌨️",
        "Clear": "🌙",
        "Mostly Clear": "🌙",
        "Partly Cloudy": "🌙",
        "Hazy Moonlight": "🌙"
    }

    return weather_icons.get(icon_phrase, icon_phrase)
