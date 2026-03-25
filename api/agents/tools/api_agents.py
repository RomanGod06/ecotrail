import os
import requests
import environ
from pathlib import Path

# --- BULLETPROOF ENV SETUP ---
BASE_DIR = Path(__file__).resolve().parent
while not os.path.exists(os.path.join(BASE_DIR, '.env')) and BASE_DIR.parent != BASE_DIR:
    BASE_DIR = BASE_DIR.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

def get_weather_and_aqi(lat: float, lon: float, location_name: str) -> str:
    """
    Fetches exact weather and air quality for a specific coordinate.
    
    Args:
        lat: Latitude of the location.
        lon: Longitude of the location.
        location_name: The human-readable name of the place or trail.
    """
    api_key = '0ca3a2820ab59bf6f9632e7a0b154f44'
    
    try:
        # 1. Fetch Weather using exact coordinates
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        w_res = requests.get(weather_url, params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}, timeout=4)
        w_data = w_res.json()
        
        if w_res.status_code != 200:
            return f"API Error: {w_data.get('message')}"
            
        temp = w_data['main']['temp']
        wind_speed = w_data['wind']['speed']
        description = w_data['weather'][0]['description']

        # 2. Fetch AQI
        aqi_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        a_res = requests.get(aqi_url, params={"lat": lat, "lon": lon, "appid": api_key}, timeout=4)
        a_data = a_res.json()
        aqi = a_data['list'][0]['main']['aqi']

        # 3. Simple Safety Logic
        if aqi >= 4 or wind_speed > 15.0:
            safety = "Danger 🔴"
        elif temp < -5 or "rain" in description.lower():
            safety = "Caution 🟡"
        else:
            safety = "Safe 🟢"

        # 4. Return formatted data back to Gemini
        return (f"Data for {location_name} (Lat: {lat}, Lon: {lon}): "
                f"Temp: {temp}°C, Weather: {description}, Wind: {wind_speed}m/s, AQI: {aqi}. "
                f"Status: {safety}")

    except Exception as e:
        return f"Error fetching data: {str(e)}"