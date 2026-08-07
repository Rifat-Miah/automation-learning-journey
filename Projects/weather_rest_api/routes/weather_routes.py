from flask import Blueprint, request, jsonify, current_app
from services.weather_service import WeatherService
import logging

weather_bp = Blueprint('weather', __name__) #Create blueprint
logger = logging.getLogger(__name__)

weather_service = WeatherService()  #Initialize services

