import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from config import Config

logger = logging.getlogger(__name__)

class WeatherDatabase:    #JSON Based Database for Weather History
    def __init__(self):   #Initialize the database
        self.data_file = Config.HISTORY_FILE
        self.data = []
        self._load_data()

    def _load_data(self):  # Load data from JSON file
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info(f"Loaded {len(self.data)} history records")
            else:
                self.data = []
                self._save_data()
                logger.info("Created new history file")
        except json.JSONDecodeError as e:
            logger.error(f"Error loading history data: {e}")
            self.data = []
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            self.data = []
    def save_data(self):     # Save data to JSON file
        try:
            Config.DATA_DIR.mkdir(exist_ok=True) # Ensure directory exists
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved {len(self.data)} records to history")
        except Exception as e:
            logger.error(f"Error saving history data: {e}")   
    def save_search_history(self, city: str, weather_data: Dict, units: str = 'metric') -> int:
        """
        Save a weather search to history
        Args:
            city: City name
            weather_data: Weather data dictionary
            units: Units used
            
        Returns:
            Index of the saved record
        """
        record = {
            'id': len(self.data),
            'city': city,
            'units': units,
            'timestamp': datetime.now().isoformat(),
            'data': weather_data,
            'summary': f"{weather_data['weather']['description']} - {weather_data['temperature']['current']}{weather_data['temperature']['unit']}"
        }
        
        self.data.append(record)
        self._save_data()
        logger.info(f"Saved weather search for {city} to history")
        return len(self.data) - 1
    def get_history(self, limit: int = 10, offset: int = 0) -> List[Dict]:
        """
        Get weather history with pagination
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of history records
        """
        sorted_data = sorted(      # Sort by timestamp descending (newest first)
            self.data,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        start = offset  # Apply pagination
        end = offset + limit
        return sorted_data[start:end]
    
    def get_history_count(self) -> int:  #Get total number of history records
        return len(self.data)
