from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import numpy as np
import joblib
import time
import json
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings
from .logger import logger

# Load the ML model with error handling
try:
    model = joblib.load(settings.MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    raise e

# Input validation
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

@app.get("/")
def root():
    return {"message": "API is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/ready")
def readiness_check():
    try:
        _ = model.predict(np.zeros((1,4)))
        return {"status": "ready"}
    except:
        return {"status": "not ready"}

@app.post("/predict")
def predict(data: IrisData):
    try:
        input_data = np.array([[ 
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]])

        prediction = model.predict(input_data)[0]

        logger.info(
            f"Prediction={prediction} for data={input_data.tolist()}"
        )

        return {"prediction": int(prediction)}

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

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
        status_code = 500
        logger.error(f"Request error: {e}")
        raise e
    
    process_time = (time.time() - start_time) * 1000
    log_details={
        "method": method,
        "url": url,
        "client_ip": client_ip,
        "status_code": status_code,
        "process_time_ms": f"{process_time:.2f}"
    }
    logger.info(json.dumps(log_details))
    response.headers["X-Process-Time-ms"] = f"{process_time:.2f}"

    return response
