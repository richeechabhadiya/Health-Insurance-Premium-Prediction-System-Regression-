from fastapi import FastAPI
import pandas as pd
import numpy as np
from src.utils.predict import Predictor # Use your existing class!

app = FastAPI()

# Initialize your actual predictor logic
# This ensures np.expm1() and categorical handling are applied correctly
predictor = Predictor("models/best_model.pkl")

@app.get("/")
def home():
    return {"message": "Insurance Premium API is Running"}

@app.post("/predict")
def predict_premium(data: dict):
    try:
        # 1. Convert incoming JSON to DataFrame
        df = pd.DataFrame([data])
        
        # 2. Use the Predictor class methods directly
        # This handles the feature alignment and the log-reverse (np.expm1)
        prediction = predictor.predict(df)
        
        return {"premium": float(prediction[0])}
    except Exception as e:
        return {"error": str(e)}