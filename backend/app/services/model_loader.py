# app/services/model_loader.py

from pathlib import Path
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models" / "demo_bert"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -------------------------------------------------
# Load tokenizer & model safely
# -------------------------------------------------
try:
    tokenizer = BertTokenizer.from_pretrained(str(MODEL_DIR))
    model = BertForSequenceClassification.from_pretrained(str(MODEL_DIR))
    model.to(device)
    model.eval()
except Exception as e:
    print("ERROR LOADING MODEL:", e)
    tokenizer = None
    model = None


# -------------------------------------------------
# Prediction function
# -------------------------------------------------
def predict(text: str):
    if not model or not tokenizer:
        return {"prediction": "UNKNOWN", "confidence": 0.0}

    if not text.strip():
        return {"prediction": "UNKNOWN", "confidence": 0.0}

    try:
        inputs = tokenizer(
            text, return_tensors="pt", truncation=True, padding=True, max_length=256
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            probs = softmax(outputs.logits, dim=-1)

        pred = torch.argmax(probs, dim=1).item()
        confidence = probs[0, pred].item()

        return {
            "prediction": "FAKE" if pred == 1 else "TRUE",  # key renamed for frontend
            "confidence": round(confidence, 4),
        }

    except Exception as e:
        print("ERROR DURING PREDICTION:", e)
        return {"prediction": "UNKNOWN", "confidence": 0.0}
