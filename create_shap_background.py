import pandas as pd
import joblib
import os
from pathlib import Path

# Set paths based on your structure
base_dir = Path(__file__).resolve().parent
data_path = base_dir / "data" / "split" / "X_train.csv"
model_dir = base_dir / "models"

if not data_path.exists():
    print(f"❌ Error: {data_path} not found. Check your 'data/split' folder!")
else:
    print("📂 Loading training data to create SHAP background...")
    X_train = pd.read_csv(data_path)
    
    # Take 100 samples for the background
    background = X_train.sample(n=min(100, len(X_train)), random_state=42)
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(background, model_dir / "shap_background.pkl")
    print(f"✅ Success! Background saved to {model_dir}/shap_background.pkl")
