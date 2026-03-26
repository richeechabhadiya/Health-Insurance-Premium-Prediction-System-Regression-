import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# Setup paths relative to src/explainability/
ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = ROOT / "models" / "best_model.pkl"
BG_PATH = ROOT / "models" / "shap_background.pkl"

def generate_background():
    if not MODEL_PATH.exists():
        print(f"❌ Error: Model not found at {MODEL_PATH}")
        return

    # Load model to get feature names
    bundle = joblib.load(MODEL_PATH)
    feature_cols = bundle["feature_cols"]
    
    print("🎲 Generating realistic background samples...")
    
    # Create 50 realistic rows so SHAP values are non-zero
    data = []
    for _ in range(50):
        row = {col: 0 for col in feature_cols}
        row.update({
            "age": np.random.randint(20, 70),
            "seniority_insured": np.random.randint(1, 20),
            "exposure_time": np.random.uniform(0.5, 1.0),
            "n_insured_mun": np.random.randint(200, 5000),
            "cost_claims_year": np.random.uniform(500, 5000)
        })
        data.append(row)
    
    X_bg = pd.DataFrame(data)
    
    # Ensure all columns exist and are in right order
    for col in feature_cols:
        if col not in X_bg.columns:
            X_bg[col] = 0
    X_bg = X_bg[feature_cols]

    # Save
    joblib.dump(X_bg, BG_PATH)
    print(f"✅ Success! SHAP background saved at: {BG_PATH}")

if __name__ == "__main__":
    generate_background()
