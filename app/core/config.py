import os
from dotenv import load_dotenv

# .env file se variables ko system memory mein load karo
load_dotenv()

class Settings:
    PROJECT_NAME: str = "PyTorch ML Serving Platform"
    
    # System memory se Redis ka URL uthao, agar nahi mile toh local fallback lagao
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

# Poore project mein use karne ke liye settings ka ek instance bana liya
settings = Settings()