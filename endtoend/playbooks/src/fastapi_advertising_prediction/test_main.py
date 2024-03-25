from fastapi.testclient import TestClient

try:
    from main import app
except:
    from fastapi_advertising_prediction.main import app

client = TestClient(app)


def test_predict_advertising():
    response = client.post("/prediction/advertising", json={
        "TV": 230.1,
        "Radio": 37.8,
        "Newspaper": 69.2
    })

    assert response.status_code == 200
    assert isinstance(response.json()['result'], float), 'Result wrong type!'
