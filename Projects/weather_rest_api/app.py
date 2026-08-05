import sys
import logging
from pathlib import Path
from flask import Flask, jsonify
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
logging = logging.grtLogger(__name__)

#Initialize Flask app
app = Flask(__name__)
#Load Configuration
config = get_config()
app.config.from_object(config)