from fastapi import FastAPI
from app.api import predict  # Apna route import kiya

app = FastAPI(title="MLOps Serving Platform")

# Extension cord ko switchboard mein lagaya
app.include_router(predict.router)

@app.get("/")
def health_check():
    return {"status": "System is running perfectly, Boss! (Refactored Version)"}