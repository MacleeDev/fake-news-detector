# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.predict import router as predict_router


app = FastAPI(title="Fake News Detector AI")


# -----------------------------
# CORS CONFIG (VERY IMPORTANT)
# -----------------------------
origins = [
    "http://localhost",
    "http://localhost:5500",  # VS Code Live Server
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "*",  # allow all (OK for development)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Include prediction routes
# -----------------------------
app.include_router(predict_router, prefix="/api")


# -----------------------------
# Optional root endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Fake News Detector API is running"}
