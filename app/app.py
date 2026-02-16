from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os

# Load model relative to file location (container-safe)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Iris Classifier API",
    version="1.0.0"
)

# ---------- Schemas ----------
class PredictionRequest(BaseModel):
    sepal_length: float = Field(..., gt=0)
    sepal_width: float = Field(..., gt=0)
    petal_length: float = Field(..., gt=0)
    petal_width: float = Field(..., gt=0)

class PredictionResponse(BaseModel):
    prediction: int
    confidence: float


# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    features = np.array([[
        request.sepal_length,
        request.sepal_width,
        request.petal_length,
        request.petal_width
    ]])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = float(max(probabilities))

    return PredictionResponse(
        prediction=int(prediction),
        confidence=confidence
    )
