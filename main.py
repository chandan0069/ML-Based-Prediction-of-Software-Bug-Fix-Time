import joblib
import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from schema import BugInput, PredictionOutput



# Model loading
MODEL_PATH = "model/best_rf_pipeline.joblib"
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    except FileNotFoundError:
        raise RuntimeError(
            f"Model file not found at '{MODEL_PATH}'. "
            "Run the export cell in your notebook first."
        )
    yield
    model = None


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Bug Fix Time Predictor",
    description="Predicts whether a Jira bug will be resolved in < 8 days (Short) or >= 8 days (Long).",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Feature engineering — mirrors Cell 3 of the notebook exactly
# ---------------------------------------------------------------------------
def parse_components(x: str) -> int:
    """Replicates the n_components logic from the notebook."""
    if not x or pd.isna(x):
        return 0
    x = str(x).strip()
    if x.startswith("["):
        try:
            return len(eval(x))
        except Exception:
            pass
    return len([c for c in x.split(",") if c.strip()])


def build_features(data: BugInput) -> pd.DataFrame:
    summary = data.summary.strip()
    description = (data.description or "").strip()
    created = pd.to_datetime(data.created_date)

    text = (summary + " . " + description).replace(r"\s+", " ")

    row = {
        "text":          text,
        "priority":      data.priority,
        "summary_len":   len(summary),
        "desc_len":      len(description),
        "n_components":  parse_components(data.components),
        "created_dow":   created.dayofweek,
        "created_hour":  created.hour,
        "created_month": created.month,
    }
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "Bug Fix Time Predictor is running."}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionOutput, tags=["prediction"])
def predict(data: BugInput):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    try:
        X = build_features(data)
        confidence = float(model.predict_proba(X)[0][1])

        THRESHOLD = 0.80                          # ← add this line
        label = int(confidence >= THRESHOLD)      # ← replace the old predict line

        result_map = {1: "Short (< 8 days)", 0: "Long (>= 8 days)"}
        return PredictionOutput(
            prediction=result_map[label],
            confidence=round(confidence, 4),
            label=label,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")