# Machine Learning Prediction API

This project provides a production-ready machine learning inference API using FastAPI and Docker.  
It takes a trained model and exposes it as a simple, versioned HTTP service that can be deployed locally or inside containerized environments.

The goal of this project is to demonstrate how a small ML model can be converted into a reliable microservice with real-world engineering features such as versioning, request latency tracking, structured logs, health checks, and configuration management.

---

## Quick Start

Clone the repository and build the Docker image:

```bash
docker build -t ml-api .
docker run -p 8000:8000 ml-api
```

Open the API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Why This Project Exists

Most ML projects stop after training a model.  
This service focuses on the deployment side—how to host a model in a clean, maintainable, and production-oriented way.

It demonstrates patterns that scale well:
- separating training from inference
- supporting multiple versions of a model
- structured logging suitable for large systems
- health checks for orchestration environments
- containerized delivery for portability

---

## Architecture Overview

```
Client Request
      |
      v
 FastAPI Service
      |
      |-- Loads correct model version (cached)
      |
      v
  Model Predict
      |
      v
  JSON Response
```

Key internal components:
- model loader with caching  
- versioned model directory  
- request logging middleware  
- latency measurement  
- health/readiness probes  

---

## Features

### Model Serving
- Predicts using joblib-serialized models.
- Stores multiple model versions (for example, `v1`, `v2`) in a dedicated directory.
- Uses in-memory caching to avoid repeated disk loads.

### Logging and Monitoring
- Structured JSON logs for easier analysis.
- Middleware that records request duration.
- Suitable for container platforms and log collection systems.

### Health and Readiness
- `/health` endpoint confirms application availability.
- `/ready` endpoint verifies model inference is functional.

### Configuration
- `.env` file for runtime configuration.
- Pydantic `BaseSettings` for validated environment reads.

### Optional Security
- Supports API key validation through request headers.

### Containerization
- Multi-stage Dockerfile to keep the runtime image minimal.
- Docker health check to verify container health.

---

## Project Structure

```
ml-api/
 ├── app/
 │    ├── main.py
 │    ├── config.py
 │    ├── logger.py
 │    ├── models/
 │    │    ├── v1.joblib
 │    │    ├── v2.joblib (optional)
 │    ├── requirements.txt
 ├── train_model.py
 ├── Dockerfile
 ├── .env
 ├── README.md
```

---

## API Endpoints

### Root
GET `/`  
Returns a simple response confirming the service is active.

### Health Check
GET `/health`  
Indicates whether the application is running.

### Readiness Check
GET `/ready`  
Attempts a lightweight prediction to confirm model readiness.

### Predict
POST `/predict?version=v1`  

Request example:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Response example:

```json
{
  "prediction": 0,
  "model_version": "v1"
}
```

### Switch Model Version
GET `/switch-model/{version}`  
Loads and caches the requested version.

---

## Training the Model

Run the training script:

```bash
python train_model.py
```

This will create files such as:

```
models/v1.joblib
```

Additional versions can be created by retraining and saving models with new names.

---

## Running with Docker

Build the image:

```bash
docker build -t ml-api .
```

Run the container:

```bash
docker run -p 8000:8000 ml-api
```

Access automatic API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Environment Variables

Example `.env` file:

```
APP_NAME="ML Prediction API"
APP_VERSION="1.0"
MODEL_DIR="models"
DEFAULT_VERSION="v1"
API_KEY="secret123"
```

---

## Troubleshooting

If the API returns "model not found":
- Ensure the model file exists under `models/` with the correct name.
- Verify the `MODEL_DIR` setting in `.env`.

If Docker reports the container as unhealthy:
- Check that `/health` is reachable inside the container.

If predictions fail:
- Confirm the model supports `predict` on a 4-feature input.

---

## Author

DharshanKanth

