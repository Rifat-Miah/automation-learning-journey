import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
from flask import jsonify, request
import time

#Configure logger
logger = logging.getLogger(__name__)


class WeatherFormatter:
    
    #Utility class for formatting weather data
    @staticmethod
    def format_temperature(temp: float, units: str = 'metric') -> Dict[str, Any]:
        """
        Format temperature with appropriate units
        Args:
            temp: Temperature value
            units: 'metric' or 'imperial'
        Returns:
            Dictionary with temperature and unit
        """
        unit_symbol = '°C' if units == 'metric' else '°F'
        return {
            'value': round(temp, 1),
            'unit': unit_symbol,
            'unit_code': units
        }

    @staticmethod
    def format_wind_speed(speed: float, units: str = 'metric') -> Dict[str, Any]:
        """
        Format wind speed with appropriate units
        Args:
            speed: Wind speed value
            units: 'metric' or 'imperial'
        Returns:
            Dictionary with speed and unit
        """
        unit = 'm/s' if units == 'metric' else 'mph'
        return {
            'value': round(speed, 1),
            'unit': unit,
            'unit_code': units
        }

    @staticmethod
    def format_timestamp(timestamp: int, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
        """
        Convert timestamp to readable format
        Args:
            timestamp: Unix timestamp
            format_str: Output format string
        Returns:
            Formatted time string
        """
        return datetime.fromtimestamp(timestamp).strftime(format_str)


class ResponseBuilder:
    #Utility class for building consistent API responses

    @staticmethod
    def success(data: Any, message: str = "Success", status_code: int = 200) -> tuple:
        """
        Build a success response
        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code
        Returns:
            Tuple of (response_dict, status_code)
        """
        return jsonify({
            'success': True,
            'message': message,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'data': data
        }), status_code

    @staticmethod
    def error(message: str, status_code: int = 400, details: Optional[Dict] = None) -> tuple:
        """
        Build an error response
        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        Returns:
            Tuple of (response_dict, status_code)
        """
        response = {
            'success': False,
            'message': message,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        if details:
            response['details'] = details
        return jsonify(response), status_code


def log_request(f):

    #Decorator to log incoming requests
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()

        # Log request details
        logger.info(f"Request: {request.method} {request.path}")
        logger.debug(f"Headers: {dict(request.headers)}")
        logger.debug(f"Query Params: {dict(request.args)}")

        # Execute function
        response = f(*args, **kwargs)

        # Log response time
        elapsed = time.time() - start_time
        logger.info(f"Response time: {elapsed:.3f}s")

        return response
    return decorated_function


def validate_city(func):
    #Decorator to validate city parameter
    @wraps(func)
    def decorated_function(*args, **kwargs):
        city = request.args.get('city')
        if not city:
            return ResponseBuilder.error('City parameter is required', 400)

        # Clean city name
        city = city.strip()
        if len(city) < 2:
            return ResponseBuilder.error('City name must be at least 2 characters', 400)

        kwargs['city'] = city
        return func(*args, **kwargs)
    return decorated_function


class DataStore:

    def __init__(self, file_path: str = 'data/weather_history.json'):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        try:
            with open(self.file_path, 'r') as f:
                pass
        except FileNotFoundError:
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def read(self) -> list:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def write(self, data: list) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def append(self, item: Any) -> None:
        data = self.read()
        data.append(item)
        self.write(data)

    def clear(self) -> None:
        self.write([])

    def get_by_index(self, index: int) -> Optional[Any]:
        data = self.read()
        try:
            return data[index]
        except IndexError:
            return None

    def delete_by_index(self, index: int) -> Optional[Any]:
        data = self.read()
        try:
            item = data.pop(index)
            self.write(data)
            return item
        except IndexError:
            return None