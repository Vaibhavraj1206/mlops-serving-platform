import os
import torch
import torch.nn as nn
import torch.optim as optim
import mlflow
import mlflow.pytorch
from dotenv import load_dotenv

# 1. Credentials load karo
load_dotenv()
os.environ["MLFLOW_TRACKING_USERNAME"] = os.getenv("MLFLOW_TRACKING_USERNAME")
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.getenv("MLFLOW_TRACKING_PASSWORD")
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# 2. Ek bohot simple PyTorch Model banate hain
class SimpleClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # 5 input features, 2 output classes (Positive/Negative)
        self.network = nn.Linear(5, 2) 

    def forward(self, x):
        return self.network(x)

def train_model():
    # DagsHub par experiment ka naam set karo
    mlflow.set_experiment("PyTorch_Fast_Training")
    
    print("Training start ho rahi hai...")
    
    # MLflow tracking shuru!
    with mlflow.start_run() as run:
        model = SimpleClassifier()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=0.01)

        # Step A: Hyperparameters cloud par log karo
        mlflow.log_params({
            "learning_rate": 0.01,
            "epochs": 5,
            "model_type": "Simple_Linear_PyTorch"
        })

        # Step B: Training Loop (5 baar chalega)
        for epoch in range(5):
            # Hum random dummy data (10 samples) generate kar rahe hain fast training ke liye
            inputs = torch.randn(10, 5)
            labels = torch.randint(0, 2, (10,))

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # Step C: Har epoch ka 'Loss' cloud par log karo
            mlflow.log_metric("loss", loss.item(), step=epoch)
            print(f"Epoch {epoch+1}/5 | Loss: {loss.item():.4f}")

        # Step D: Poora ka poora Model DagsHub par upload kar do!
        mlflow.pytorch.log_model(
            pytorch_model=model,
            artifact_path="pytorch_model",
            registered_model_name="My_First_Cloud_Model"
        )
        
        print(f"\nTraining Complete!")
        print(f"DagsHub Run ID: {run.info.run_id}")

if __name__ == "__main__":
    train_model()