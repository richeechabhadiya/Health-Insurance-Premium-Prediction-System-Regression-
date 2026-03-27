# import joblib
# import os
# import shap
# from pathlib import Path

# CACHE = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))/'models'/'shap_explainer.pkl'

# def get_explainer(model, X_sample=None, force_rebuild=False):
#     """Return a shap.Explainer, caching to disk to avoid repeated heavy init.
#     model: trained model object
#     X_sample: small DataFrame or array used to build explainer (optional)
#     """
#     if CACHE.exists() and not force_rebuild:
#         try:
#             return joblib.load(CACHE)
#         except Exception:
#             pass

#     # build explainer (prefer TreeExplainer for tree models)
#     try:
#         expl = shap.Explainer(model)
#     except Exception:
#         expl = shap.TreeExplainer(model)

#     try:
#         joblib.dump(expl, CACHE)
#     except Exception:
#         pass

#     return expl
# # Minimal SHAP explainer wrapper with graceful fallback
# try:
#     import shap
#     _HAS_SHAP = True
# except Exception:
#     shap = None
#     _HAS_SHAP = False

# import numpy as np


# def get_explainer(model, X_sample=None):
#     """Return a SHAP explainer if available, else None."""
#     if not _HAS_SHAP:
#         return None
#     try:
#         # prefer TreeExplainer for tree models
#         expl = shap.TreeExplainer(model)
#         return expl
#     except Exception:
#         try:
#             # fallback to KernelExplainer if sample provided
#             if X_sample is not None:
#                 return shap.KernelExplainer(model.predict, X_sample)
#         except Exception:
#             return None
#     return None


# def explain_instance(explainer, X_row):
#     """Return a dict with feature->contribution or empty if not available."""
#     if explainer is None or not _HAS_SHAP:
#         # return zeros for features
#         return {c: 0.0 for c in (getattr(X_row, 'columns', None) or [])}
#     try:
#         vals = explainer.shap_values(X_row)
#         # shap_values may be array or list; handle tree regressor returning array
#         if isinstance(vals, list):
#             vals = vals[0]
#         vals = np.array(vals).reshape(-1)
#         return dict(zip(X_row.columns, vals.tolist()))
#     except Exception:
#         return {c: 0.0 for c in X_row.columns}
# src/explainability/shap_utils.py
# src/explainability/shap_utils.py


# src/explainability/shap_utils.py

import numpy as np

try:
    import shap
    _HAS_SHAP = True
except ImportError:
    shap = None
    _HAS_SHAP = False


def get_explainer(model, X_sample=None):
    """
    Build a SHAP explainer. Tries TreeExplainer first (fast, exact for
    tree-based models), then falls back to LinearExplainer, then
    KernelExplainer.
    """
    if not _HAS_SHAP:
        return None

    # ---- TreeExplainer (LightGBM, XGBoost, CatBoost, sklearn trees) ----
    try:
        expl = shap.TreeExplainer(model)
        return expl
    except Exception:
        pass

    # ---- LinearExplainer ----
    try:
        if X_sample is not None:
            expl = shap.LinearExplainer(model, X_sample)
            return expl
    except Exception:
        pass

    # ---- KernelExplainer (slow but universal) ----
    try:
        if X_sample is not None:
            # Use a small background to keep it fast
            bg = shap.sample(X_sample, min(50, len(X_sample)))
            expl = shap.KernelExplainer(model.predict, bg)
            return expl
    except Exception:
        pass

    return None


def explain_instance(explainer, X_preprocessed):
    """
    Return {feature: shap_value} dict for one row.
    X_preprocessed must already be preprocessed (numeric, correct columns).
    """
    if explainer is None or not _HAS_SHAP:
        return {c: 0.0 for c in X_preprocessed.columns}

    try:
        vals = explainer.shap_values(X_preprocessed)

        # Handle multi-output (classifiers) – take first output
        if isinstance(vals, list):
            vals = vals[0]

        vals = np.array(vals)

        # If 2-D (batch), take first row
        if vals.ndim == 2:
            vals = vals[0]

        return dict(zip(X_preprocessed.columns, vals.tolist()))
    except Exception as e:
        # Surface the error so it's visible in the UI for debugging
        raise RuntimeError(f"SHAP explain_instance failed: {e}") from e