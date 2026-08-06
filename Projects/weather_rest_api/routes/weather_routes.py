from flask import Blueprint, request, jsonify, current_app
import logging

weather_bp = Blueprint('weather', __name__)
logging = logging.getLogger(__name__)
