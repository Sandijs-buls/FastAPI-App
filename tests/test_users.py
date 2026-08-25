
from app.main import app
from app.config import settings
from jose import jwt
from app import schemas
from .database import client, session
import pytest


@pytest.fixture()
def test_user(client):
    user_data = {"email" : "hello12@gmail.com", "password" : "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user






def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == 'Hello World from FastAPI!'
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email": "hello12@gmail.com", "password": "1234"})
    user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert user.email == "hello12@gmail.com"

def test_login_user( test_user, client):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**response.json())

    #Validating the token, by decoding it and checking if the user_id in the payload matches the test_user id
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"

    assert response.status_code == 200
