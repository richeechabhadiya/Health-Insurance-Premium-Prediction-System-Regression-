# import joblib
# import pandas as pd
# import numpy as np
# from pathlib import Path

# MODEL_PATH = Path(__file__).resolve().parent.parent / "models/best_model.pkl"
# BG_PATH = Path(__file__).resolve().parent.parent / "models/shap_background.pkl"

# # Load model to get feature columns
# bundle = joblib.load(MODEL_PATH)
# feature_cols = bundle["feature_cols"]

# # Create **realistic synthetic data** for background
# def default_value(col):
#     # numeric features
#     if "age" in col:
#         return np.random.randint(18, 80)
#     if "seniority" in col:
#         return np.random.randint(0, 30)
#     if "exposure" in col or "cost_claims" in col:
#         return np.random.uniform(0, 1) * 5
#     if "n_insured" in col:
#         return np.random.randint(100, 5000)
#     # categorical features
#     if "gender" in col:
#         return np.random.choice(["M","F"])
#     if "policy" in col or "type" in col:
#         return np.random.choice(["I","II","III"])
#     if "reimbursement" in col or "new_business" in col:
#         return np.random.choice(["Yes","No"])
#     # fallback
#     return 0

# X_bg = pd.DataFrame([{col: default_value(col) for col in feature_cols} for _ in range(50)])

# # Save background
# joblib.dump(X_bg, BG_PATH)
# print(f"SHAP background saved at {BG_PATH}")



import pandas as pd
import joblib

print("Loading training data to create SHAP background...")
df = pd.read_csv("../data/processed/clean_data_final.csv")

# Drop target if exists
X = df.drop(columns=['premium'], errors='ignore')

# Sample background (100 rows)
X_bg = X.sample(n=100, random_state=42)

# Save to models folder
joblib.dump(X_bg, "../models/shap_background.pkl")
print("Success! Background saved to ../models/shap_background.pkl")