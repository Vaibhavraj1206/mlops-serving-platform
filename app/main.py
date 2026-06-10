from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import predict, models  # Apna route import kiya
from app.ml.model_loader import load_cloud_model # Naya function import kiya
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi import FastAPI, Depends, HTTPException # <-- Depends aur HTTPException add kiya
from fastapi.security import HTTPBasic, HTTPBasicCredentials # <-- Security module add kiya

# 1. Naya Lifespan Logic (Server start hote hi model laana)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Server start ho raha hai...")
    # Server start hote hi Cloud se model download karo
    load_cloud_model(version=2)
    yield
    print("🛑 Server band ho raha hai...")

# 2. FastAPI app banana (Tera purana title + Naya lifespan merge kar diya)
app = FastAPI(title="MLOps Serving Platform", lifespan=lifespan)

# --- SECURITY SYSTEM FOR METRICS ---
security = HTTPBasic()

def auth_metrics(credentials: HTTPBasicCredentials = Depends(security)):
    # Agar username ya password 'admin' nahi hai, toh API connection block kar degi
    if credentials.username != "admin" or credentials.password != "admin123":
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized", 
            headers={"WWW-Authenticate": "Basic"}
        )

Instrumentator().instrument(app).expose(app,should_gzip=True, dependencies=[Depends(auth_metrics)])

# 3. Extension cord ko switchboard mein lagaya (Purana Router)
app.include_router(predict.router, tags=["Prediction"])
app.include_router(models.router, tags=["Models"])

# 4. Tera original Health Check Route
@app.get("/")
def health_check():
    return {"status": "System is running perfectly, Boss! (Refactored Version)"}