from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import os
import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)

# Load model using joblib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "iris_model.joblib")
model = joblib.load(MODEL_PATH)

# Request body format
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

app = FastAPI()

@app.get("/")
def index():
    return {"message": "API is running 🚀"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

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
        logging.info(f"Prediction: {prediction} for input: {input_data.tolist()}")

        return {"prediction": int(prediction)}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))