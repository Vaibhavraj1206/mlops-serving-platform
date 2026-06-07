import os
import torch
import mlflow.pytorch
from app.core.config import settings

# DagsHub Cloud Credentials set karo taaki API wahan se model download kar sake
os.environ["MLFLOW_TRACKING_USERNAME"] = settings.MLFLOW_TRACKING_USERNAME
os.environ["MLFLOW_TRACKING_PASSWORD"] = settings.MLFLOW_TRACKING_PASSWORD
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

cloud_model = None

def load_cloud_model(version=1):
    """Ye function server start hote hi DagsHub se model download karega."""
    global cloud_model
    try:
        # Registry se model ka specific version mangwa rahe hain
        model_uri = f"models:/My_First_Cloud_Model/{version}"
        print(f"📥 Cloud se model download ho raha hai: {model_uri}...")
        
        cloud_model = mlflow.pytorch.load_model(model_uri)
        cloud_model.eval() # Inference mode on
        print("✅ Cloud Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")

def get_prediction(features_list: list):
    """Ye function list of numbers lega aur naye PyTorch model se result dega."""
    if cloud_model is None:
        return {"label": "Model not loaded", "score": 0.0}
        
    # Python list ko PyTorch Tensor (Matrix) mein convert karo
    tensor_input = torch.tensor([features_list], dtype=torch.float32)
    
    with torch.no_grad():
        output = cloud_model(tensor_input)
        # 2 classes mein se jiski probability zyada hai, wo nikal lo
        prediction = output.argmax(dim=1).item()
        
    return {"label": f"Class {prediction}", "score": 0.99} # Dummy confidence