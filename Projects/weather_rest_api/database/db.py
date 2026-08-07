import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from config import Config

logger = logging.getlogger(__name__)

class WeatherDatabase:    #JSON Based Database for Weather History
    def __init__(self):
        self.data_file = Config.HISTORY_FILE
        self.data = []
        self._load_data()

    def _load_data(self):
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