import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # General
    APP_NAME: str = "AI Staffing Assistant"
    APP_VERSION: str = "1.0.0"

    # Database
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DATABASE_PATH: str = os.path.join(BASE_DIR, 'employees.db')

    # API
    API_V1_STR: str = "/api/v1"

    # LLM
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

settings = Settings()
