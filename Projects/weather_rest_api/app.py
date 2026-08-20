import sys
import logging
from pathlib import Path
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config, get_config

# logging setup
logging.basicConfig(                
    level = logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.fileHandler(Config.LOG_FILE) if Config.LOG_FILE else logging.NullHandler()
    ]
)
logging = logging.getLogger(__name__)

#Initialize Flask app
app = Flask(__name__)
#Load Configuration
config = get_config()
app.config.from_object(config)

CORS(app, origins=config.CORS_ORIGINS)    #Enable CORS(app, ...) adds the needed security rules to your Flask app.

#Enable register bluprints
from routes.weather_routes import weather_bp
app.register_blueprint(weather_bp, url_prefix='/api/weather')
