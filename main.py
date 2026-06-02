from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline  # Naya AI import

app = FastAPI(title="MLOps Serving Platform")

print("Loading ML Model... Please wait...")
# Yeh line pre-trained NLP model memory mein load karti hai. 
# Pehli baar run karne par ye internet se model (~250MB) download karega.
sentiment_model = pipeline("sentiment-analysis")
print("Model Loaded Successfully!")

class MLInput(BaseModel):
    user_id: int
    data_text: str

@app.get("/")
def health_check():
    return {"status": "System is running perfectly, Boss!"}

@app.post("/predict")
def make_prediction(input_data: MLInput):
    # Dummy data ki jagah ab asli ML model tera text padhega
    ml_result = sentiment_model(input_data.data_text)
    
    return {
        "message": f"Data processed for user {input_data.user_id}",
        "your_input": input_data.data_text,
        "ai_prediction": ml_result[0]['label'],
        "ai_confidence": round(ml_result[0]['score'] * 100, 2)
    }