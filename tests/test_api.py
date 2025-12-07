from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_predict():
    res = client.post("/predict?version=v1", 
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        },
        headers={"api_key": "secret123"}
    )

    assert res.status_code == 200
    data = res.json()

    assert "prediction" in data
    assert "model_version" in data
