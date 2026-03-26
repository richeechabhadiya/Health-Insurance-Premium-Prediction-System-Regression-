def simulate(predictor, original_df, modified_df):
    try:
        orig = None
        new = None
        if predictor is not None:
            try:
                orig = float(predictor.predict(original_df)[0])
            except Exception:
                orig = None
            try:
                new = float(predictor.predict(modified_df)[0])
            except Exception:
                new = None

        savings = None
        if orig is not None and new is not None:
            savings = orig - new

        return {"original": orig, "new": new, "savings": savings}
    except Exception:
        return {"original": None, "new": None, "savings": None}