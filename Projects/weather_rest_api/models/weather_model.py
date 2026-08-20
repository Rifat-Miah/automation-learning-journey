import json
from typing import Dict, Optional, List, Any
from datetime import datetime, timezone
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
@dataclass
class WeatherHistory:

    #Data model for weather search history
    city: str
    units: str
    timestamp: str
    data: Dict[str, Any]
    summary: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {                      #Convert to dictionary
            'city': self.city,
            'units': self.units,
            'timestamp': self.timestamp,
            'data': self.data,
            'summary': self.summary
        }
    
    @classmethod
    def from_weather_data(cls, weather_data: WeatherData) -> 'WeatherHistory':
        return cls(                   #Create history entry from weather data
            city=weather_data.city,
            units=weather_data.units,
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            data=weather_data.to_dict(),
            summary=f"{weather_data.weather['description']} - {weather_data.temperature['current']}{weather_data.temperature['unit']}"
        )

class APIResponse:

    #Standard API response wrapper
    def __init__(self, success: bool, data: Any = None, message: str = "", 
                 status_code: int = 200, errors: Optional[List[str]] = None):
        self.success = success
        self.data = data
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        self.timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    def to_dict(self) -> Dict[str, Any]:
        response = {                   #Convert to dictionary for JSON response
            'success': self.success,
            'message': self.message,
            'timestamp': self.timestamp,
            'status_code': self.status_code
        }
        
        if self.success and self.data is not None:
            response['data'] = self.data
        
        if not self.success and self.errors:
            response['errors'] = self.errors
        
        return response
