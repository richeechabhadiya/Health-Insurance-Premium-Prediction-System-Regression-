import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from src.utils.predict import Predictor
import pandas as pd

def test_predictor_smoke():
    mp = Path('models') / 'best_model.pkl'
    assert mp.exists(), 'best_model.pkl missing'
    p = Predictor(str(mp))
    df = pd.DataFrame([{'age':32,'bmi':22,'smoker':'no','gender':'male','type_policy':'I','exposure_time':1.0}])
    out = p.predict(df)
    assert out is not None
    assert hasattr(out, '__len__')
