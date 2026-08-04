import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")
print(os.getenv("WEATHER_API_KEY"))