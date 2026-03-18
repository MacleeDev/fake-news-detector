# app/api/predict.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.model_loader import predict


router = APIRouter()


# -----------------------------
# Request body
# -----------------------------
class NewsText(BaseModel):
    text: str


# -----------------------------
# Response body (VERY IMPORTANT)
# -----------------------------
class PredictionResponse(BaseModel):
    prediction: str
    confidence: float


# -----------------------------
# Endpoint
# -----------------------------
@router.post("/predict", response_model=PredictionResponse)
def predict_news(data: NewsText):
    try:
        result = predict(data.text)

        # Expect result like:
        # {"prediction": "FAKE", "confidence": 0.92}
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
