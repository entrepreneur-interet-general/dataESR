import json
from src.app import app


def test_hello_world():
    test_client = app.test_client()
    response = test_client.get('/hello')
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf8')) == {'hello': 'world'}
