import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert b'Hello, World!' in response.data
