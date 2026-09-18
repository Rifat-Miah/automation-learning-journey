from flask import Flask, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime

# Import configurations and modules
from config import get_config, Config
from routes.weather_routes import weather_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('weather_api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def create_app():
    #Application factory pattern for creating Flask app
    # Get configuration
    config = get_config()
    
    # Validate configuration
    try:
        config.validate()
        config.ensure_directories()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['DEBUG'] = config.DEBUG
    app.config['CORS_ORIGINS'] = config.CORS_ORIGINS
    
    # Enable CORS
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(weather_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'name': 'Weather REST API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'weather': '/api/weather?city=London',
                'coordinates': '/api/weather/coordinates?lat=51.5&lon=-0.1',
                'history': '/api/weather/history',
                'health': '/api/weather/health'
            },
            'documentation': 'See README.md for API documentation'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found',
            'message': 'The requested endpoint does not exist'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    logger.info("Weather API application initialized successfully")
    return app

if __name__ == '__main__':
    # Get configuration
    config = get_config()
    
    # Create app
    app = create_app()
    
    # Run the application
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )