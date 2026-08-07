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

    def delete_history_item(self, index: int) -> bool:
        """
        Delete a specific history item by index
        Args:
            index: Index of the item to delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            if 0 <= index < len(self.data):
                deleted = self.data.pop(index)
                # Reindex remaining items
                for i, item in enumerate(self.data):
                    item['id'] = i
                self._save_data()
                logger.info(f"Deleted history item at index {index}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting history item: {e}")
            return False
    def clear_history(self):
        self.data = []
        self._save_data()
        logger.info("Cleared all weather history")

    def search_by_city(self, city: str) -> List[Dict]:
        """
        Search history by city name (case-insensitive)
        Args:
            city: City name to search for
            
        Returns:
            List of matching history records
        """
        city_lower = city.lower()
        return [
            item for item in self.data
            if item.get('city', '').lower() == city_lower
        ]
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the weather history
        
        Returns:
            Dictionary with statistics
        """
        if not self.data:
            return {
                'total_entries': 0,
                'unique_cities': 0,
                'most_searched_city': None,
                'avg_temperature': None
            }   
        city_counts = {}  # count cities
        temps = []
        for item in self.data:
            city = item.get('city', 'Unknown')
            city_counts[city] = city_counts.get(city, 0) + 1
            
            # Get temperature
            temp_data = item.get('data', {}).get('temperature', {})
            if temp_data:
                temps.append(temp_data.get('current', 0))
        
        most_searched = max(city_counts.items(), key=lambda x: x[1]) if city_counts else None
        
        return {
            'total_entries': len(self.data),
            'unique_cities': len(city_counts),
            'most_searched_city': most_searched[0] if most_searched else None,
            'most_searched_count': most_searched[1] if most_searched else 0,
            'avg_temperature': sum(temps) / len(temps) if temps else None
        }