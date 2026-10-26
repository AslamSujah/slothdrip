import numpy as np

# Soil index -> moisture-holding coefficient (higher = holds water longer)
SOILS = {"Sandy": 0, "Potting Mix": 1, "Clay": 2, "Coco Coir": 3}
RETENTION = {0: 0.35, 1: 0.6, 2: 0.85, 3: 0.75}
FEATURES = ["days_since_watered", "avg_temp_c", "humidity_pct", "soil_type_index"]

def _simulate(n=600, seed=0):
    """Bootstrap 'historical' records from a simple physical drying model.
    Replace with real CSV logs (same 4 columns + needs_water) when you have them."""
    rng = np.random.default_rng(seed)
    days = rng.uniform(0, 14, n)
    temp = rng.uniform(5, 40, n)
    hum = rng.uniform(15, 95, n)
    soil = rng.integers(0, 4, n)
    ret = np.vectorize(RETENTION.get)(soil)
    evap = 0.04 + 0.004 * (temp - 5) + 0.002 * (100 - hum) / 10
    moisture = 1.0 - days * evap / ret + rng.normal(0, 0.05, n)
    y = (moisture < 0.45).astype(int)
    return np.c_[days, temp, hum, soil], y

_clf = None

def _get():
    global _clf
    if _clf is None:
        from tabpfn import TabPFNClassifier
        X, y = _simulate()
        _clf = TabPFNClassifier()
        _clf.fit(X, y)  # in-context "fit": no gradient training
    return _clf

def predict_water(days, temp, hum, soil_name):
    x = np.array([[days, temp, hum, SOILS[soil_name]]])
    return float(_get().predict_proba(x)[0][1])
