import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Base directory
BASE_DIR=Path(__file__).resolve().parent.parent

# API Settings
CYBOTRADE_API_KEY = os.getenv("CYBOTRADE_API_KEY")
CYBOTRADE_API_URL = "https://api.datasource.cybotrade.rs/"
CRYPTOQUANT_API_URL = "https://api.datasource.cybotrade.rs/cryptoquant"
GLASSNODE_API_URL = "https://api.datasource.cybotrade.rs/glassnode"
COINGLASS_API_URL = "https://api.datasource.cybotrade.rs/coinglass"

# Data settings
DATE_INTERVAL = 7
DEFAULT_RESPONSE_LIMIT = 10000