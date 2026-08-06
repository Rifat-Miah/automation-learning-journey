import requests
import json
from typing import Dict, Optional, Tuple
from datetime import datetime
import logging
from config import get_config
logger = logging.getLogger(__name__)
config = get_config

class WeatherService:       # fetching and processing weather data
    def __init__(self):
        self.api_key = config.WEATHER_API_KEY
        self.base_url = config.WEATHER_API_URL

        if not self.api_key:
            raise ValueError("Weather API key not configured.")

    def get_weather(self, city: str, units: str = 'metric') -> Dict:
        """
        Fetch weather data for a given city
        Args:
            city: Name of the city
            units: 'metric' or 'imperial'
            
        Returns:
            Dict containing formatted weather data
            
        Raises:
            ValueError: If city not found or invalid response
            ConnectionError: If network issues occur
            TimeoutError: If request times out
        """
        try:
            logger.debug(f"Fetching weather for city: {city}, units: {units}")
            params = {
                'q': city.strip(),
                'appid': self.api_key,
                'units': units
            }
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            if response.status_code == 404:
                raise ValueError(f"City '{city}' not found. Please check the spelling and try again.")
            elif response.status_code == 401:
                raise ValueError("Invalid API key. Please check your configuration.")
            elif response.status_code == 429:
                raise ValueError("API rate limit exceeded. Please wait and try again.")
            elif response.status_code != 200:
                raise ConnectionError(f"API returned status code {response.status_code}")

            #Parse JSON response
            data = response.json()
            return self._format_weather_data(data, units)              # Format and return weather data

        except requests.Timeout as e:
            logger.error(f"Connection Error: {str(e)}")
            raise TimeoutError("Request timed out. Please try again later.")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise ValueError("Invalid response received from weather service.")
        except Exception as e:
            logger.error(f"Unexpected error in get_weather: {str(e)}")
            raise
    def get_weather_by_coordinates(self, lat: float, lon: float, units: str = 'metric') -> Dict:
        """
        Fetch weather data using latitude and longitude
        Args:
            lat: Latitude
            lon: Longitude
            units: 'metric' or 'imperial'
            
        Returns:
            Dict containing formatted weather data
        """
        try:
            logger.debug(f"Fetching weather for coordinates: ({lat}, {lon}), units: {units}")
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': units
            }

            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )

            response.raise_for_status()
            data = response.json()
            return self._format_weather_data(data, units)
        except requests.RequestException as e:
            logger.error(f"Error fetching weather by coordinates: {str(e)}")
            raise

    def _format_weather_data(self, data: Dict, units: str) -> Dict:
        """
        Format raw weather API response into a clean, structured dictionary
        
        Args:
            data: Raw weather data from API
            units: 'metric' or 'imperial'
            
        Returns:
            Formatted weather data dictionary
        """
        # Determine units
        temp_unit = '°C' if units == 'metric' else '°F'
        speed_unit = 'm/s' if units == 'metric' else 'mph'

        #convert Timestamps
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
        current_time = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')

        # Format weather data
        formatted = {
            'city': data['name'],
            'country': data['sys']['country'],
            'coordinates': {
                'lat': data['coord']['lat'],
                'lon': data['coord']['lon']
            },
            'temperature': {
                'current': round(data['main']['temp'],1 ),
                'feels_like': round(data['main']['feels_like'], 1),
                'min': round(data['main']['temp_min', 1]),
                'max': round(data['main']['temp_max', 1]),
                'unit': temp_unit
            },
            'humidity': data['main']['humididty'],
            'pressure': data['main']['pressure'],
            'wind': {
                'speed': round(data['wind']['speed'], 1),
                'degree': data['wind'].get('deg'),
                'unit': speed_unit
            },
            'clouds': data['clouds']['all'],
            'weather': {
                'main': data['weather'][0]['main'],
                'description':data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon']
            },
            'sunrise': sunrise,
            'sunset': sunset,
            'current_time': current_time,
            'units': units,
            'raw': data  # Keep raw data for debugging/advanced use
        }
        return formatted

    def validate_city(self, city: str) -> bool:
        """
        Validate if a city exists (without fetching full weather data)
        Args:
            city: City name to validate
            
        Returns:
            True if city exists, False otherwise
        """
        try:
            params= {
                'q': city,
                'appid': self.api_key,
                'limit': 1
            }
            response = requests.get(
                'http://api.openweathermap.org/geo/1.0/direct',
                params=params,
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                return len(data) > 0
            return False
        except Exception:
            return False