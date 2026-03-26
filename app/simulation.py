# from src.simulation.scenario import simulate as _simulate

# def simulate(predictor, original_df, modified_df):
#     try:
#         return _simulate(predictor, original_df, modified_df)
#     except Exception:
#         return None

def simulate(predictor, inputs, new_inputs):
    base = predictor.predict(inputs)[0]
    new  = predictor.predict(new_inputs)[0]

    return {
        "original": base,
        "new": new,
        "saving": base - new
    }