# Insurance Premium Predictor — Demo

Quick start (Linux):

1. Create and activate venv

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

2. Run the app

```bash
./run.sh
# then open http://localhost:8501
```

3. Run unit tests

```bash
pip install pytest
pytest -q
```

Notes:
- If you don't want to install `weasyprint` remove it from `requirements.txt`.
- The Streamlit app uses absolute model paths to reliably load the saved model.
