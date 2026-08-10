import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()   # load environment variables

class Config:
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_URL = os.getenv("WEATHER_API_URL","http://api.openweathermap.org/data/2.5/weather")

    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV=os.getenv('FLASK_ENV', 'development')
    DEBUG =os.getenv('FLASK_DEBUG', '1') == '1'

    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / os.getenv('DATA_DIR', 'data')
    HISTORY_FILE = DATA_DIR / os.getenv('HISTORY_FILE', 'weather_history.json')   

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = BASE_DIR / os.getenv('LOG_FILE', 'logs/weather_api.log')

    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    DEFAULT_UNITS = 'metric'    # or 'imerial'
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOG_FILE.parent.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is required. Please check your .env file")
        return True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    
    # In production, CORS should be more restrictive
    CORS_ORIGINS = os.getenv('PROD_CORS_ORIGINS', 'https://yourdomain.com').split(',')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATA_DIR = Config.BASE_DIR / 'tests' / 'test_data'
    HISTORY_FILE = DATA_DIR / 'test_history.json'

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
def get_config():
    """Get the appropriate configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_map.get(env, DevelopmentConfig)
