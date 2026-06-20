import threading
import time
from datetime import datetime

import requests

from structures.dataclasses import ForecastEntry, WeatherCondition, WeatherReading

_WMO_CONDITION = {
    0: WeatherCondition.CLEAR, 1: WeatherCondition.CLEAR,
    2: WeatherCondition.PARTLY_CLOUDY, 3: WeatherCondition.CLOUDY,
    45: WeatherCondition.FOG, 48: WeatherCondition.FOG,
    51: WeatherCondition.RAIN, 53: WeatherCondition.RAIN, 55: WeatherCondition.RAIN,
    56: WeatherCondition.RAIN, 57: WeatherCondition.RAIN,
    61: WeatherCondition.RAIN, 63: WeatherCondition.RAIN, 65: WeatherCondition.RAIN,
    66: WeatherCondition.RAIN, 67: WeatherCondition.RAIN,
    71: WeatherCondition.SNOW, 73: WeatherCondition.SNOW, 75: WeatherCondition.SNOW,
    77: WeatherCondition.SNOW,
    80: WeatherCondition.RAIN, 81: WeatherCondition.RAIN, 82: WeatherCondition.RAIN,
    85: WeatherCondition.SNOW, 86: WeatherCondition.SNOW,
    95: WeatherCondition.THUNDERSTORM, 96: WeatherCondition.THUNDERSTORM,
    99: WeatherCondition.THUNDERSTORM,
}
 
 
class WeatherData(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.temperature_c = 0
        self.condition = WeatherCondition.CLOUDY
        self.feels_like_c = 0
        self.hourly = ForecastEntry("", WeatherCondition.CLOUDY, 0)
        self.daily = ForecastEntry("", WeatherCondition.CLOUDY, 0)
 
    def run(self):
        while True:
            try:
                self._fetch()
            except Exception:
                pass
            time.sleep(300)
 
    def _fetch(self):
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": 52.7641416,
                "longitude": 13.4126907,
                "current": "temperature_2m,apparent_temperature,weather_code",
                "hourly": "temperature_2m,weather_code",
                "daily": "weather_code,temperature_2m_max",
                "timezone": "auto",
                "forecast_days": 2,
            },
            timeout=10,
        )
        data = resp.json()
        current = data["current"]
        
        hourly_start = datetime.fromisoformat(data["hourly"]["time"][0])
        now = datetime.fromisoformat(current["time"])
        now_idx = int((now - hourly_start).total_seconds() // 3600)
        near_idx = min(now_idx + 2, len(data["hourly"]["time"]) - 1)
 
        self.temperature_c = current["temperature_2m"]
        self.feels_like_c = current["apparent_temperature"]
        self.condition = _WMO_CONDITION.get(current["weather_code"], WeatherCondition.CLOUDY)
        hour_time_str = data["hourly"]["time"][near_idx]
        hour_dt = datetime.fromisoformat(hour_time_str)
        self.hourly = ForecastEntry(
            label=hour_dt.strftime("%Hh"),
            condition=_WMO_CONDITION.get(
                data["hourly"]["weather_code"][near_idx],
                WeatherCondition.CLOUDY
            ),
            temperature_c=data["hourly"]["temperature_2m"][near_idx],
        )
        tomorrow_date_str = data["daily"]["time"][1]
        tomorrow_dt = datetime.fromisoformat(tomorrow_date_str)
        self.daily = ForecastEntry(
            label=tomorrow_dt.strftime("%a"),
            condition=_WMO_CONDITION.get(
                data["daily"]["weather_code"][1],
                WeatherCondition.CLOUDY
            ),
            temperature_c=data["daily"]["temperature_2m_max"][1],
        )
 
    def get_data(self):
        return WeatherReading(
            temperature_c=self.temperature_c,
            condition=self.condition,
            feels_like_c=self.feels_like_c,
            hourly=self.hourly,
            daily=self.daily,
        )
