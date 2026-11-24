from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).parent / "model.joblib"

@lru_cache
def _load():
    return joblib.load(MODEL_PATH)

def predict(values: dict) -> tuple[str,float]:
    bundle = _load()
    features = bundle["features"]
    row = [values[f.replace(" ", "_")] for f in features]
    x = pd.DataFrame([row], columns=features)

    model = bundle["model"]
    label = bundle["classes"][int(model.predict(x)[0])] # predict(x) given array of output
    prob_design = float(model.predict_proba(x)[0][1]) # oredict_proba return probabilities of classes in array
    return label, prob_design