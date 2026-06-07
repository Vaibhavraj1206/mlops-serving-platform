from fastapi import APIRouter, BackgroundTasks
from app.schemas.predict_schema import MLInput
from app.ml.model_loader import get_prediction
from app.core.redis import generate_cache_key, get_cached_prediction, set_cached_prediction
# Naya worker import kiya
from app.workers.background_loggers import log_inference_to_db

router = APIRouter()

# Dependency injection: path function mein 'background_tasks: BackgroundTasks' add kiya
@router.post("/predict")
def make_prediction(input_data: MLInput, background_tasks: BackgroundTasks):
    input_dict = {"text": input_data.features}
    cache_key = generate_cache_key(input_dict)
    cached_result = get_cached_prediction(cache_key)
    
    if cached_result:
        # CACHE HIT! Background task lagao
        background_tasks.add_task(
            log_inference_to_db, 
            input_data.user_id, 
            input_data.features, 
            cached_result['label']
        )
        
        return {
            "message": f"Data processed for user {input_data.user_id}",
            "your_input": input_data.features,
            "ai_prediction": cached_result['label'],
            "ai_confidence": cached_result['confidence'],
            "source": "Redis Cache ⚡"
        }
        
    # CACHE MISS! AI Model run karo
    ml_result = get_prediction(input_data.features)
    
    prediction_to_save = {
        "label": ml_result['label'],
        "confidence": round(ml_result['score'] * 100, 2)
    }
    
    set_cached_prediction(cache_key, prediction_to_save, ttl_seconds=3600)
    
    # Naye AI Result ke liye bhi Background task lagao
    background_tasks.add_task(
        log_inference_to_db, 
        input_data.user_id, 
        input_data.features, 
        prediction_to_save['label']
    )
    
    return {
        "message": f"Data processed for user {input_data.user_id}",
        "your_input": input_data.features,
        "ai_prediction": prediction_to_save['label'],
        "ai_confidence": prediction_to_save['confidence'],
        "source": "AI Model 🤖"
    }