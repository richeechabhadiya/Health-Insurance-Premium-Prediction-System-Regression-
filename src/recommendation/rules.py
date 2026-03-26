def get_recommendations(row, current_premium, predictor=None):
    """Return a list of human-friendly suggestions and optional estimated savings.

    row can be a dict or pandas Series. predictor is optional; if provided, a simulated
    new premium will be computed for some suggestions.
    """
    suggestions = []
    try:
        # normalize access
        if hasattr(row, 'to_dict'):
            data = row.to_dict()
        else:
            data = dict(row)

        # Suggest quitting smoking
        if data.get('smoker') and str(data.get('smoker')).lower() in ['yes','y','true','1']:
            # simulate
            if predictor is not None:
                try:
                    new = data.copy()
                    new['smoker'] = 'no'
                    new_p = predictor.predict(pd.DataFrame([new]))[0]
                    savings = current_premium - new_p
                    suggestions.append(f'Quit smoking → Estimated saving ₹{round(savings,2)}')
                except Exception:
                    suggestions.append('Quit smoking → Likely large reduction in premium')
            else:
                suggestions.append('Quit smoking → Likely large reduction in premium')

        # Suggest reducing BMI if overweight
        try:
            bmi = float(data.get('bmi', 0))
            if bmi > 25:
                if predictor is not None:
                    try:
                        new = data.copy()
                        new['bmi'] = max(18.5, bmi - 3)
                        new_p = predictor.predict(pd.DataFrame([new]))[0]
                        savings = current_premium - new_p
                        suggestions.append(f'Reduce BMI by 3 → Estimated saving ₹{round(savings,2)}')
                    except Exception:
                        suggestions.append('Reduce BMI to normal range → Likely moderate reduction')
                else:
                    suggestions.append('Reduce BMI to normal range → Likely moderate reduction')
        except Exception:
            pass

        # Generic suggestion: check policy type if present
        if 'type_policy' in data and data.get('type_policy') != 'I':
            suggestions.append('Check alternative policy types — some variants may be cheaper')

    except Exception:
        # on any error return a small default suggestion list
        suggestions = ['Review smoking status', 'Evaluate BMI and lifestyle', 'Compare policy types']

    return suggestions