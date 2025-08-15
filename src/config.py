import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
MODE = os.getenv('MODE', 'manual').lower()
HANDLER = os.getenv('HANDLER', '.save')
DOWNLOAD_PATH = "downloads/"
