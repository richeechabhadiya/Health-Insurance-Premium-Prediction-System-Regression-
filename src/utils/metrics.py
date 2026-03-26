# """
# src/utils/metrics.py  —  FIXED: thresholds match actual data range (~800–4000)
# """
# import joblib
# import os
# from pathlib import Path

# REPO_ROOT = Path(__file__).resolve().parents[2]


# def risk_level(premium):
#     """
#     ⚠️  FIXED: old thresholds (>20000, >12000) were wrong for this dataset.
#     Actual premium range is roughly 800–4000.
#     Adjust these if your data has a different scale.
#     """
#     if premium is None:
#         return "UNKNOWN ❓"
#     try:
#         p = float(premium)
#     except Exception:
#         return "UNKNOWN ❓"

#     if p > 3000:
#         return "HIGH 🔴"
#     elif p > 1800:
#         return "MEDIUM 🟡"
#     else:
#         return "LOW 🟢"


# def compare_with_avg(premium):
#     """
#     ⚠️  FIXED: use absolute path so it works regardless of Streamlit's cwd.
#     """
#     if premium is None:
#         return "Premium not available"
#     try:
#         avg_path = REPO_ROOT / "models" / "avg_premium.pkl"
#         if not avg_path.exists():
#             # fallback: compute from y_test split
#             y_path = REPO_ROOT / "data" / "split" / "y_test.csv"
#             if not y_path.exists():
#                 return "Average premium data not available"
#             import pandas as pd
#             avg = float(pd.read_csv(str(y_path)).values.ravel().mean())
#         else:
#             avg = float(joblib.load(str(avg_path)))

#         diff_pct = ((float(premium) - avg) / avg) * 100
#         direction = "higher" if diff_pct >= 0 else "lower"
#         return f"{abs(diff_pct):.1f}% {direction} than average (avg: ₹{avg:.0f})"
#     except Exception:
#         return "Average premium data not available"


"""
src/utils/metrics.py  —  FIXED thresholds + absolute paths
"""
import joblib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def risk_level(premium):
    """
    FIXED: old thresholds (>20000 HIGH, >12000 MEDIUM) were wrong.
    Actual dataset premium range is ~800–4000.
    """
    if premium is None:
        return "UNKNOWN ❓"
    p = float(premium)
    if p > 3000:
        return "HIGH 🔴"
    if p > 1800:
        return "MEDIUM 🟡"
    return "LOW 🟢"


def compare_with_avg(premium):
    """FIXED: uses absolute path so it works from any cwd."""
    if premium is None:
        return "Premium not available"
    try:
        avg_pkl = REPO_ROOT / "models" / "avg_premium.pkl"
        if avg_pkl.exists():
            avg = float(joblib.load(str(avg_pkl)))
        else:
            y_path = REPO_ROOT / "data" / "split" / "y_test.csv"
            if not y_path.exists():
                return "Average premium data not available"
            import pandas as pd
            avg = float(pd.read_csv(str(y_path)).values.ravel().mean())

        diff = ((float(premium) - avg) / avg) * 100
        direction = "higher" if diff >= 0 else "lower"
        return f"{abs(diff):.1f}% {direction} than average (avg: ₹{avg:.0f})"
    except Exception:
        return "Average premium data not available"