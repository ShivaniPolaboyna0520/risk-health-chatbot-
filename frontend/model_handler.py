import numpy as np
import joblib

model = joblib.load("model/diabetes_model.pkl")
scaler = joblib.load("model/scaler.pkl")

def predict_diabetes(features):
    arr = np.array(features).reshape(1, -1)
    scaled = scaler.transform(arr)
    prediction = model.predict(scaled)[0]
    probability = model.predict_proba(scaled)[0][1]
    return int(prediction), round(probability, 2)
