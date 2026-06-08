import time
from fastapi import APIRouter, BackgroundTasks
from app.schemas.predict_schema import MLInput
from app.ml.model_loader import get_prediction, get_current_model_info
from app.core.redis import generate_cache_key, get_cached_prediction, set_cached_prediction
from app.workers.background_loggers import log_inference_to_db

router = APIRouter()

@router.post("/predict")
def make_prediction(input_data: MLInput, background_tasks: BackgroundTasks):
    start_time = time.time() # Latency track karne ke liye timer start
    
    input_dict = {"features": input_data.features}
    cache_key = generate_cache_key(input_dict)
    cached_result = get_cached_prediction(cache_key)
    
    # Current loaded model ka version nikal lo
    model_info = get_current_model_info()
    version = model_info["version"] if model_info else 1
    
    if cached_result:
        # CACHE HIT!
        latency = (time.time() - start_time) * 1000
        background_tasks.add_task(
            log_inference_to_db, 
            user_id=input_data.user_id,
            prediction=cached_result['label'],
            confidence=cached_result['confidence'],
            model_version=version,
            latency_ms=latency,
            cached=True
        )
        
        return {
            "message": "Success",
            "prediction": cached_result['label'],
            "confidence": cached_result['confidence'],
            "source": "Redis Cache ⚡",
            "latency_ms": round(latency, 2)
        }
        
    # CACHE MISS! AI Model run karo
    ml_result = get_prediction(input_data.features)
    latency = (time.time() - start_time) * 1000
    
    prediction_to_save = {
        "label": ml_result['label'],
        "confidence": ml_result['score']
    }
    
    set_cached_prediction(cache_key, prediction_to_save, ttl_seconds=3600)
    
    # AI Result ko Database mein bhejo
    background_tasks.add_task(
        log_inference_to_db, 
        user_id=input_data.user_id,
        prediction=prediction_to_save['label'],
        confidence=prediction_to_save['confidence'],
        model_version=version,
        latency_ms=latency,
        cached=False
    )
    
    return {
        "message": "Success",
        "prediction": prediction_to_save['label'],
        "confidence": prediction_to_save['confidence'],
        "source": "AI Model 🤖",
        "latency_ms": round(latency, 2)
    }