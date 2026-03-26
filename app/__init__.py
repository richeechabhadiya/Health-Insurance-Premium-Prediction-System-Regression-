"""app package for the Streamlit application.

This file makes the `app` directory a Python package so internal imports
like `from app.ui_components import ...` resolve correctly when running
the Streamlit app.
"""

__all__ = ["app", "ui_components", "explanation"]
