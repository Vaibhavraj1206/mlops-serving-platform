from fastapi import APIRouter
from app.schemas.predict_schema import MLInput
from app.ml.model_loader import get_prediction

# APIRouter humara mini-FastAPI hai
router = APIRouter()

@router.post("/predict")
def make_prediction(input_data: MLInput):
    # Yahan humne ML logic ko call kiya jo doosri file mein hai
    ml_result = get_prediction(input_data.data_text)
    
    return {
        "message": f"Data processed for user {input_data.user_id}",
        "your_input": input_data.data_text,
        "ai_prediction": ml_result['label'],
        "ai_confidence": round(ml_result['score'] * 100, 2)
    }