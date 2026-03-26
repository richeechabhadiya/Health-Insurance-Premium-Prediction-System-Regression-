# import pandas as pd
# from src.recommendation.rules import get_recommendations as _get_recommendations

# def get_recommendations(row, current_premium, predictor=None):
#     # accept pandas Series or dict
#     if hasattr(row, 'to_dict'):
#         data = row.to_dict()
#     else:
#         data = dict(row)
#     # Call core rules
#     return _get_recommendations(data, current_premium, predictor=predictor)


def generate_suggestions(inputs, predictor, base_pred):
    suggestions = []

    # Example: change policy
    for p in ["I", "II", "III"]:
        if p != inputs["type_policy"]:
            new_inputs = inputs.copy()
            new_inputs["type_policy"] = p
            new_pred = predictor.predict(new_inputs)[0]

            if new_pred < base_pred:
                diff = base_pred - new_pred
                suggestions.append(
                    f"Switch to Policy {p} → Save ₹{diff:.0f}"
                )

    return suggestions