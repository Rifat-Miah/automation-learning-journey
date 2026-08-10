from flask import Blueprint, request, jsonify, current_app
from services.weather_service import WeatherService
from database.db import WeatherDatabase
import logging

weather_bp = Blueprint('weather', __name__) #Create blueprint
logger = logging.getLogger(__name__)

weather_service = WeatherService()  #Initialize services
weather_db = WeatherDatabase()

@weather_bp.route('', methods=['GET'])
def get_weather():
    """
    Get weather for a city
    
    Query Parameters:
        city: City name (required)
        units: 'metric' or 'imperial' (optional, default: metric)
    """
    city = request.args.get('city')
    try:
        units = request.args.get('units', 'metric')
        
        if not city:
            return jsonify({
                'success': False,
                'error': 'City parameter is required',
                'message': 'Please provide a city name'
            }), 400
        
        if units not in ['metric', 'imperial']:
            return jsonify({
                'success': False,
                'error': 'Invalid units parameter',
                'message': 'Units must be "metric" or "imperial"'
            }), 400
        weather_data = weather_service.get_weather(city, units)     # Get weather data
        weather_db.save_search_history(city, weather_data, units)   # Save to history

        logger.info(f"Weather fetched for city: {city}")
        
        return jsonify({
            'success': True,
            'data': weather_data,
            'timestamp': weather_data.get('current_time'),
            'message': f"Weather data retrieved successfully for {city}"
        }), 200
    except ValueError as e:
        logger.warning(f"Value error for city {city}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'City not found',
            'message': str(e)
        }), 404
    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Connection error',
            'message': str(e)
        }), 503
    except TimeoutError as e:
        logger.error(f"Timeout error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Timeout error',
            'message': str(e)
        }), 504
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'Failed to fetch weather data'
        }), 500
    
@weather_bp.route('/coordinates', methods=['GET'])
def get_weather_by_coords():
    """
    Get weather by coordinates
    
    Query Parameters:
        lat: Latitude (required)
        lon: Longitude (required)
        units: 'metric' or 'imperial' (optional, default: metric)
    """
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        units = request.args.get('units', 'metric')
        
        if not lat or not lon:
            return jsonify({
                'success': False,
                'error': 'Latitude and longitude are required',
                'message': 'Please provide both lat and lon parameters'
            }), 400
        
        # Validate coordinates
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid coordinates',
                'message': 'Latitude and longitude must be valid numbers'
            }), 400
        
        weather_data = weather_service.get_weather_by_coordinates(lat, lon, units)
        
        return jsonify({
            'success': True,
            'data': weather_data,
            'message': 'Weather data retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching weather by coordinates: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch weather',
            'message': str(e)
        }), 500

@weather_bp.route('/history', methods=['GET'])
def get_history():
    """
    Get weather search history
    
    Query Parameters:
        limit: Number of records to return (optional, default: 10)
        offset: Offset for pagination (optional, default: 0)
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        if limit < 1 or limit > 100:
            return jsonify({
                'success': False,
                'error': 'Invalid limit parameter',
                'message': 'Limit must be between 1 and 100'
            }), 400
        
        history = weather_db.get_history(limit=limit, offset=offset)
        
        return jsonify({
            'success': True,
            'data': history,
            'count': len(history),
            'total': weather_db.get_history_count(),
            'message': 'History retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve history',
            'message': str(e)
        }), 500

@weather_bp.route('/history/<int:index>', methods=['DELETE'])
def delete_history_item(index):
    """
    Delete a specific history item
    
    Path Parameters:
        index: Index of the history item to delete
    """
    try:
        result = weather_db.delete_history_item(index)
        
        if result:
            return jsonify({
                'success': True,
                'message': f'History item at index {index} deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Index not found',
                'message': f'No history item found at index {index}'
            }), 404
            
    except Exception as e:
        logger.error(f"Error deleting history item: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete history item',
            'message': str(e)
        }), 500

@weather_bp.route('/history/clear', methods=['DELETE'])
def clear_history():
    """Clear all weather history"""
    try:
        weather_db.clear_history()
        return jsonify({
            'success': True,
            'message': 'All weather history cleared successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear history',
            'message': str(e)
        }), 500

@weather_bp.route('/settings', methods=['PUT'])
def update_settings():
    """
    Update default settings
    
    Body:
        {
            "default_units": "metric" or "imperial"
        }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided',
                'message': 'Please provide settings data'
            }), 400
        
        # Validate settings
        if 'default_units' in data:
            if data['default_units'] not in ['metric', 'imperial']:
                return jsonify({
                    'success': False,
                    'error': 'Invalid units',
                    'message': 'default_units must be "metric" or "imperial"'
                }), 400
        
        # Update settings (in a real app, this would update a database)
        # For now, we'll just return success
        logger.info(f"Settings updated: {data}")
        
        return jsonify({
            'success': True,
            'data': data,
            'message': 'Settings updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating settings: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update settings',
            'message': str(e)
        }), 500
