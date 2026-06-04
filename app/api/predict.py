from fastapi import APIRouter
from app.schemas.predict_schema import MLInput
from app.ml.model_loader import get_prediction
# Naye Redis imports
from app.core.redis import generate_cache_key, get_cached_prediction, set_cached_prediction

router = APIRouter()

@router.post("/predict")
def make_prediction(input_data: MLInput):
    # Step 1: Input text ko dictionary mein convert kiya hash banane ke liye
    input_dict = {"text": input_data.data_text}
    
    # Step 2: Unique Hash Key generate ki
    cache_key = generate_cache_key(input_dict)
    
    # Step 3: Redis (Cache) mein check kiya
    cached_result = get_cached_prediction(cache_key)
    
    if cached_result:
        # CACHE HIT! Bina AI chalaye turant answer wapas bhej do
        return {
            "message": f"Data processed for user {input_data.user_id}",
            "your_input": input_data.data_text,
            "ai_prediction": cached_result['label'],
            "ai_confidence": cached_result['confidence'],
            "source": "Redis Cache ⚡"  # Pata chalega ki superfast speed kahan se aayi
        }
        
    # Step 4: CACHE MISS! Agar Redis mein nahi mila, toh asli AI model chalao
    ml_result = get_prediction(input_data.data_text)
    
    # Data ko thoda format kar lete hain
    prediction_to_save = {
        "label": ml_result['label'],
        "confidence": round(ml_result['score'] * 100, 2)
    }
    
    # Step 5: Naye AI result ko Redis mein save kar do (1 Ghante / 3600 sec ke liye)
    set_cached_prediction(cache_key, prediction_to_save, ttl_seconds=3600)
    
    # User ko answer de do
    return {
        "message": f"Data processed for user {input_data.user_id}",
        "your_input": input_data.data_text,
        "ai_prediction": prediction_to_save['label'],
        "ai_confidence": prediction_to_save['confidence'],
        "source": "AI Model 🤖"  # Pata chalega ki fresh calculation hui hai
    }