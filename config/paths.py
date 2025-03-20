from config.settings import BASE_DIR

# Data directory
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Logs directory
LOG_DIR = BASE_DIR / "logs"
API_LOG_DIR = LOG_DIR / "api_integrator"
ETL_LOG_DIR = LOG_DIR / "etl"
MODEL_LOG_DIR = LOG_DIR / "models"

# Models directory
MODEL_DIR = BASE_DIR / "models"
REGIME_DETECTION_MODEL_DIR = MODEL_DIR / "regime_detection"
TRADING_MODEL_DIR = MODEL_DIR / "trading_bot"
REINFORCEMENT_LEARNING_MODEL_DIR = MODEL_DIR / "reinforcement-learning"


DIRECTORIES = [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    LOG_DIR,
    API_LOG_DIR,
    ETL_LOG_DIR,
    MODEL_LOG_DIR,
    MODEL_DIR,
    REGIME_DETECTION_MODEL_DIR,
    TRADING_MODEL_DIR,
    REINFORCEMENT_LEARNING_MODEL_DIR
]

def create_directories():
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)

create_directories()

