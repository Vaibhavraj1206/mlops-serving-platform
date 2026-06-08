from fastapi import APIRouter, HTTPException
from app.ml.model_loader import get_current_model_info, switch_model

router = APIRouter()

@router.get("/models")
def list_models():
    """Check karo ki API mein abhi kaunsa model loaded hai."""
    model_info = get_current_model_info()
    if not model_info:
        return {"status": "No model loaded"}

    return {
        "status": "active",
        "current_version": model_info["version"],
        "loaded_at": model_info["loaded_at"]
    }

@router.post("/models/switch")
def switch_model_version(version: int):
    """Bina server restart kiye MLflow se naya model load karo."""
    current = get_current_model_info()
    previous_version = current["version"] if current else None

    # Model switch karne ki koshish karo
    success = switch_model(version)

    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Version {version} load nahi ho saka. DagsHub par check karo ki kya ye version exist karta hai."
        )

    return {
        "success": True,
        "message": f"Model v{previous_version} se v{version} par switch ho gaya! Cache flushed ⚡",
        "current_version": version
    }