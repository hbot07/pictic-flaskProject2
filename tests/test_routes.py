import os
import pytest

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login(client):
    response = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    assert b'login' in response.data


def test_upload(client):
    response = client.post('/login', data=dict(
        username='parth',
        password='password'
    ), follow_redirects=True)

    with open('test_image.jpg', 'rb') as image:
        response = client.post('/upload', data=dict(
            title='Test Image',
            image=image
        ), follow_redirects=True)

    # assert response.status_code == 200
    assert os.path.exists('static/uploads/Test_Image_admin_')  # the filename will have a random integer appended to it
