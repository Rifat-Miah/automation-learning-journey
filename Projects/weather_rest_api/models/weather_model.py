import json
from typing import Dict, Optional, List, Any
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class WeatherData:
    city: str
    country: str
    temperature: Dict[str, Any]
    humidity: int
    presssure: int
    wind: Dict[str, Any]
    clouds: int
    weather: Dict[str, Any]
    sunrise: str
    sunset: str
    current_time: str
    units: str = 'metric'
    coordinates: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:     #Convert to dictionary
        return {
            'city': self.city,
            'country': self.country,
            'coordinates': self.coordinates,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind': self.wind,
            'clouds': self.clouds,
            'weather': self.weather,
            'sunrise': self.sunrise,
            'sunset': self.sunset,
            'current_time': self.current_time,
            'units': self.units
        }
