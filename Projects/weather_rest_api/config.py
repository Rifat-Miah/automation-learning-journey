import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()   # load environment variables

class Config:
    #Api Configuration
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    WEATHER_API_URL = os.getenv("WEATHER_API_URL","http://api.openweathermap.org/data/2.5/weather")

    #flask configuration
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV=os.getenv('FLASK_ENV', 'development')
    DEBUG =os.getenv('FLASK_DEBUG', '1') == '1'

    #SERVER CONFIGURATION
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))

    # Data Configuration
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / os.getenv('DATA_DIR', 'data')
    HISTORY_FILE = DATA_DIR / os.getenv('HISTORY_FILE', 'weather_history.json')   

    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = BASE_DIR / os.getenv('LOG_FILE', 'logs/weather_api.log')

    #CORS CONFIGURATIOPN
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    #Defult Units
    DEFAULT_UNITS = 'metric'    # or 'imerial'

