# import numpy as np
# import matplotlib.pyplot as plt

# def explain_with_shap(predictor, X):
#     """Backward-compatible: return simple list explanation (or None).
#     This uses explain_with_shap_plot under the hood.
#     """
#     out = explain_with_shap_plot(predictor, X)
#     if out is None:
#         return None
#     contrib_list, fig = out
#     return contrib_list

# def explain_with_shap_plot(predictor, X, top_k=5):
#     """Return (contrib_list, matplotlib_fig) or None if SHAP not available.

#     contrib_list: [{'feature': name, 'shap': value}, ...]
#     fig: matplotlib.figure.Figure
#     """
#     try:
#         import shap
#     except Exception:
#         return None

#     try:
#         model = predictor.model
#         # get cached explainer if available
#         try:
#             from src.explainability.shap_explainer import get_explainer
#             explainer = get_explainer(model)
#         except Exception:
#             try:
#                 explainer = shap.Explainer(model)
#             except Exception:
#                 explainer = shap.TreeExplainer(model)

#         # prepare data for explainer
#         X_proc = predictor.preprocess(X.copy())
#         # shap can accept numpy arrays; try to get values
#         if hasattr(X_proc, 'values'):
#             arr = X_proc if isinstance(X_proc, np.ndarray) else X_proc.values
#         else:
#             arr = np.asarray(X_proc)

#         shap_values = explainer(arr)
#         # take first row
#         vals = shap_values.values[0]
#         # feature names: prefer predictor.feature_cols
#         if getattr(shap_values, 'feature_names', None) is not None:
#             names = list(shap_values.feature_names)
#         elif predictor.feature_cols is not None:
#             names = list(predictor.feature_cols)
#         else:
#             names = [f'f{i}' for i in range(len(vals))]

#         contrib = list(zip(names, vals))
#         contrib = sorted(contrib, key=lambda x: -abs(x[1]))[:top_k]
#         contrib_list = [{'feature': f, 'shap': float(v)} for f, v in contrib]

#         # build simple horizontal bar chart
#         feats = [c['feature'] for c in contrib_list][::-1]
#         vals_plot = [c['shap'] for c in contrib_list][::-1]
#         colors = ['#1f77b4' if v >= 0 else '#ff7f0e' for v in vals_plot]
#         fig, ax = plt.subplots(figsize=(6, max(2, len(feats)*0.6)))
#         ax.barh(feats, vals_plot, color=colors)
#         ax.set_xlabel('SHAP value')
#         ax.set_title('Top feature contributions')
#         plt.tight_layout()

#         return contrib_list, fig
#     except Exception:
#         return None



import shap
import numpy as np

def get_shap_values(predictor, df):
    X = predictor.preprocess(df)

    explainer = shap.Explainer(predictor.model)
    shap_values = explainer(X)

    values = shap_values.values[0]
    features = predictor.feature_cols

    result = sorted(
        zip(features, values),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:10]

    return result