import os
import sys

from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
print(sys.path)
from service.model_api_serving.api_source.main import app, model_loader
import socket

print(TestClient.__module__)

def resolve_host_gateway():
    try:
        return socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        return "172.17.0.1"  # fallback for Linux Docker host


def load_model():
    import mlflow
    import os
    mlflow.set_tracking_uri(f"http://{resolve_host_gateway()}:5001")
    print(f"Using MLflow URI: {mlflow.get_tracking_uri()}")
    return mlflow.pyfunc.load_model("models:/stroke_prediction_model/Staging")

app.dependency_overrides[model_loader] = load_model
client = TestClient(app)

def test_invalid_data_input_for_preds(sample_wrong_data):
    print('Start pytest: test valid data input to model for predictions')
    response = client.post(url="/predict", json=sample_wrong_data)

    assert response.status_code == 422
    print(response.json())
    assert response.json() == {"detail": [{'loc': ['body', 'Age'], 'msg': 'value is not a valid integer', 'type': 'type_error.integer'}, {'loc': ['body', 'Bmi'], 'msg': 'value is not a valid float', 'type': 'type_error.float'}]}

def test_invalid_data_format_for_preds(sample_wrong_format_data):
    print('Start pytest: test valid data format to model for predictions')
    response = client.post(url="/predict", json=sample_wrong_format_data)

    assert response.status_code == 422
    print(response.json())
    assert response.json() == {'detail': [{'loc': ['body', 'Bod'], 'msg': 'extra fields not permitted', 'type': 'value_error.extra'}, {'loc': ['body', 'Name'], 'msg': 'extra fields not permitted', 'type': 'value_error.extra'}, {'loc': ['body', 'Sex'], 'msg': 'extra fields not permitted', 'type': 'value_error.extra'}]}
def test_correct_inference(sample_data):
    print('Start pytest: test model correctness')
    response = client.post(url="/predict", json=sample_data)

    assert response.status_code == 200
    assert response.json() == {"stroke": 0}



