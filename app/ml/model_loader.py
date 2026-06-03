from transformers import pipeline

print("Loading ML Model... Please wait...")
sentiment_model = pipeline("sentiment-analysis")
print("Model Loaded Successfully!")

def get_prediction(text: str):
    # Yeh function AI model ko chalayega aur result return karega
    result = sentiment_model(text)
    return result[0]