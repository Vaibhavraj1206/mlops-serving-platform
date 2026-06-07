from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import predict  # Apna route import kiya
from app.ml.model_loader import load_cloud_model # Naya function import kiya

# 1. Naya Lifespan Logic (Server start hote hi model laana)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Server start ho raha hai...")
    # Server start hote hi Cloud se model download karo
    load_cloud_model(version=1)
    yield
    print("🛑 Server band ho raha hai...")

# 2. FastAPI app banana (Tera purana title + Naya lifespan merge kar diya)
app = FastAPI(title="MLOps Serving Platform", lifespan=lifespan)

# 3. Extension cord ko switchboard mein lagaya (Purana Router)
app.include_router(predict.router)

# 4. Tera original Health Check Route
@app.get("/")
def health_check():
    return {"status": "System is running perfectly, Boss! (Refactored Version)"}