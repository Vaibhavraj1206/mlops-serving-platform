import hashlib
import json
import redis
from app.core.config import settings

# 1. Cloud Redis se connection banana
# decode_responses=True ka matlab hai ki Redis hume bytes ki jagah normal string dega
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def generate_cache_key(input_data: dict) -> str:
    """Dictionary se unique MD5 hash banata hai"""
    data_str = json.dumps(input_data, sort_keys=True)
    return hashlib.md5(data_str.encode("utf-8")).hexdigest()

def get_cached_prediction(cache_key: str):
    """Redis se data nikalne ki koshish karta hai (Cache Hit/Miss)"""
    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data) # String ko wapas dictionary bana diya
        return None
    except Exception as e:
        print(f"Redis GET Error: {e}")
        return None

def set_cached_prediction(cache_key: str, prediction_data: dict, ttl_seconds: int = 3600):
    """Redis mein data save karta hai (Default TTL = 1 Ghanta / 3600 sec)"""
    try:
        # Dictionary ko string banakar save karte hain
        redis_client.set(
            name=cache_key,
            ex=ttl_seconds,
            value=json.dumps(prediction_data)
        )
        return True
    except Exception as e:
        print(f"Redis SET Error: {e}")
        return False

def flush_prediction_cache():
    """Naya model aane par purane saare cached results delete kar deta hai."""
    try:
        # Redis mein jo bhi keys hain, sab delete kar do
        redis_client.flushdb()
        print("🗑️ Redis Cache flushed completely! Naye model ke liye ready.")
        return True
    except Exception as e:
        print(f"Redis Flush Error: {e}")
        return False

# --- CLOUD CONNECTION TEST ---
if __name__ == "__main__":
    print("Testing Redis Connection...")
    test_key = "test_hello"
    test_val = {"message": "Cloud connection successful!"}
    
    # Save kar rahe hain (10 seconds ke liye)
    set_cached_prediction(test_key, test_val, ttl_seconds=10)
    print("Data saved to Upstash Redis!")
    
    # Wapas nikal rahe hain
    result = get_cached_prediction(test_key)
    print("Data retrieved:", result)