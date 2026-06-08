import os
import torch
import mlflow.pytorch
from datetime import datetime
from app.core.config import settings
from app.core.redis import flush_prediction_cache

os.environ["MLFLOW_TRACKING_USERNAME"] = settings.MLFLOW_TRACKING_USERNAME
os.environ["MLFLOW_TRACKING_PASSWORD"] = settings.MLFLOW_TRACKING_PASSWORD
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

# Global state banayenge taaki version aur loading time bhi yaad rahe
_model_state = {
    "model": None,
    "version": None,
    "loaded_at": None
}

def load_cloud_model(version=1):
    """Ye function server start hote hi ya switch hone par DagsHub se model download karega."""
    global _model_state
    try:
        model_uri = f"models:/My_First_Cloud_Model/{version}"
        print(f"📥 Cloud se model download ho raha hai: {model_uri}...")
        
        new_model = mlflow.pytorch.load_model(model_uri)
        new_model.eval() # Inference mode on
        
        # State update karo
        _model_state["model"] = new_model
        _model_state["version"] = version
        _model_state["loaded_at"] = datetime.now().isoformat()
        
        print(f"✅ Cloud Model v{version} loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def get_current_model_info():
    """API ko dikhane ke liye ki abhi kaunsa model chal raha hai."""
    if _model_state["model"] is None:
        return None
    return {"version": _model_state["version"], "loaded_at": _model_state["loaded_at"]}

def switch_model(version: int):
    """Zero-downtime model switcher."""
    print(f"🔄 Switching model to version {version}...")
    success = load_cloud_model(version)
    if success:
        # Agar model successfully badal gaya, toh purana cache saaf kar do!
        flush_prediction_cache()
    return success

def get_prediction(features_list: list):
    """Same purana inference logic"""
    if _model_state["model"] is None:
        return {"label": "Model not loaded", "score": 0.0}
        
    tensor_input = torch.tensor([features_list], dtype=torch.float32)
    with torch.no_grad():
        output = _model_state["model"](tensor_input)
        prediction = output.argmax(dim=1).item()
        
    return {"label": f"Class {prediction}", "score": 0.99}