import requests
import json

def fetch_data():
    lat, lon = 42.3001, -83.0165
    
    # Endpoints
    weather_url = "https://api.open-meteo.com/v1/forecast"
    aqi_url = "https://api.open-meteo.com/v1/air-quality"
    geo_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"

    try:
        session = requests.Session()
        headers = {'User-Agent': 'WeatherApp/1.0'}

        # A. Location Data
        geo_res = session.get(geo_url, headers=headers)
        geo_data = geo_res.json()
        location_info = {
            "city": geo_data.get('address', {}).get('city', 'Unknown'),
            "country": geo_data.get('address', {}).get('country', 'Unknown'),
            "display_name": geo_data.get('display_name')
        }

        # B. Weather Data
        w_params = {
            "latitude": lat, "longitude": lon,
            "current": ["temperature_2m", "wind_speed_10m", "apparent_temperature", "precipitation", "rain", "showers", "weather_code"],
            "timezone": "auto"
        }
        w_data = session.get(weather_url, params=w_params).json()

        # C. AQI Data
        aqi_params = {
            "latitude": lat, "longitude": lon,
            "current": ["us_aqi", "pm2_5"]
        }
        a_data = session.get(aqi_url, params=aqi_params).json()

        # --- COMBINING INTO ONE OBJECT ---
        # We use the | operator to merge dictionaries (Python 3.9+)
        final_report = {
            "location": location_info,
            "weather": w_data.get("current"),
            "air_quality": a_data.get("current"),
            "metadata": {
                "timezone": w_data.get("timezone"),
                "elevation": w_data.get("elevation")
            }
        }

        # Print as pretty JSON
        print(json.dumps(final_report, indent=4))
        return final_report

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

#fetch_data()


def mock_fetch_data():
    return {
    "location": {
        "city": "Windsor",
        "country": "Canada",
        "display_name": "Hanna Street, Walkerville, Windsor, Southwestern Ontario, Ontario, N8X 2S0, Canada"
    },
    "weather": {
        "time": "2026-01-20T18:30",
        "interval": 900,
        "temperature_2m": -11.9,
        "wind_speed_10m": 17.1,
        "apparent_temperature": -18.2,
        "precipitation": 0.0,
        "rain": 0.0,
        "showers": 0.0,
        "weather_code": 1
    },
    "air_quality": "null",
    "metadata": {
        "timezone": "America/Toronto",
        "elevation": 188.0
    }
}

#print(mock_fetch_data())

def wmo_weather_codes():
    return {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight",
    81: "Rain showers: Moderate",
    82: "Rain showers: Violent",
    85: "Snow showers: Slight",
    86: "Snow showers: Heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}