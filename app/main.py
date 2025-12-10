from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel, Field
import numpy as np
import joblib
import time
import json
import os
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse

from .config import settings
from .logger import logger


# ----------------------------------------
# MODEL CACHE (prevents reloading each request)
# ----------------------------------------
model_cache = {}


# ----------------------------------------
# MODEL LOADING WITH VERSIONING
# ----------------------------------------
def load_model(version: str):
    """Load model from disk based on version."""
    model_path = os.path.join(settings.MODEL_DIR, f"{version}.joblib")
    logger.info(f"Attempting to load model: {model_path}")

    if not os.path.exists(model_path):
        logger.error(f"Model file not found: {model_path}")
        raise FileNotFoundError(f"Model version '{version}' not found.")

    return joblib.load(model_path)


def get_model(version: str):
    """Return cached model or load if not cached."""
    if version not in model_cache:
        logger.info(f"Caching model version: {version}")
        model_cache[version] = load_model(version)
    return model_cache[version]


# Preload default model at startup
get_model(settings.DEFAULT_VERSION)


# ----------------------------------------
# FastAPI Initialization
# ----------------------------------------
class IrisData(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )



# ----------------------------------------
# ROUTES
# ----------------------------------------
@app.get("/")
def root():
    return {"message": "API is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    """Check if the default model can make predictions."""
    try:
        default_model = get_model(settings.DEFAULT_VERSION)
        _ = default_model.predict(np.zeros((1, 4)))
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {"status": "not ready"}


@app.get("/switch-model/{version}")
def switch_model(version: str):
    """Manually switch loaded model version."""
    try:
        get_model(version)  # Cache load
        return {"status": "success", "loaded_version": version}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/predict")
@limiter.limit("10/minute")
def predict(
    request: Request,
    data: IrisData,
    version: str = settings.DEFAULT_VERSION,
    api_key: str = Header(None)
):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        model_to_use = get_model(version)

        input_data = np.array([[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]])

        prediction = model_to_use.predict(input_data)[0]

        # Confidence score
        if hasattr(model_to_use, "predict_proba"):
            proba = model_to_use.predict_proba(input_data).max()
        else:
            proba = None

        logger.info(
            f"Prediction={prediction}, version={version}, data={input_data.tolist()}"
        )

        return {
            "prediction": int(prediction),
            "confidence": float(proba) if proba is not None else None,
            "model_version": version
        }

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))



# ----------------------------------------
# REQUEST LOGGING MIDDLEWARE
# ----------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    method = request.method
    url = request.url.path
    client_ip = request.client.host

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        logger.error(f"Request error: {e}")
        raise e

    process_time = (time.time() - start_time) * 1000  # ms
    log_details = {
        "method": method,
        "url": url,
        "client_ip": client_ip,
        "status_code": status_code,
        "process_time_ms": f"{process_time:.2f}"
    }

    logger.info(json.dumps(log_details))

    response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"

    return response
