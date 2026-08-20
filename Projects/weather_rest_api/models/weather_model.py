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
    @classmethod
    def from_api_response(cls, api_data: Dict[str, Any], units: str = 'matric') -> 'WeatherData':
        """
        Create WeatherData instance from OpenWeatherMap API response
        Args:
            api_data: Raw API response
            units: 'metric' or 'imperial'   
        Returns:
            WeatherData instance
        """
        temp_unit = '°C' if units == 'metric' else '°F'
        speed_unit = 'm/s' if units == 'metric' else 'mph'

        sunrise = datetime.fromtimestamp(api_data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.fromtimestamp(api_data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
        current_time = datetime.fromtimestamp(api_data['dt']).strftime('%Y-%m-%d %H:%M:%S')
        
        return cls(
            city=api_data['name'],
            country=api_data['sys']['country'],
            coordinates={
                'lat': api_data['coord']['lat'],
                'lon': api_data['coord']['lon']
            },
            temperature={
                'current': round(api_data['main']['temp'], 1),
                'feels_like': round(api_data['main']['feels_like'], 1),
                'min': round(api_data['main']['temp_min'], 1),
                'max': round(api_data['main']['temp_max'], 1),
                'unit': temp_unit
            },
            humidity=api_data['main']['humidity'],
            pressure=api_data['main']['pressure'],
            wind={
                'speed': round(api_data['wind']['speed'], 1),
                'degree': api_data['wind'].get('deg'),
                'unit': speed_unit
            },
            clouds=api_data['clouds']['all'],
            weather={
                'main': api_data['weather'][0]['main'],
                'description': api_data['weather'][0]['description'].capitalize(),
                'icon': api_data['weather'][0]['icon']
            },
            sunrise=sunrise,
            sunset=sunset,
            current_time=current_time,
            units=units
        )

