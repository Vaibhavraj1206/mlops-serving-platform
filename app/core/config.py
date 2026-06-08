import os
from dotenv import load_dotenv

# .env file se variables ko system memory mein load karo
load_dotenv()

class Settings:
    PROJECT_NAME: str = "PyTorch ML Serving Platform"
    
    # System memory se Redis ka URL uthao, agar nahi mile toh local fallback lagao
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI")
    MLFLOW_TRACKING_USERNAME: str = os.getenv("MLFLOW_TRACKING_USERNAME")
    MLFLOW_TRACKING_PASSWORD: str = os.getenv("MLFLOW_TRACKING_PASSWORD")
    DATABASE_URL: str = os.getenv("DATABASE_URL")

# Poore project mein use karne ke liye settings ka ek instance bana liya
settings = Settings()