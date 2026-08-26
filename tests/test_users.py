
from app.main import app
from app.config import settings
from jose import jwt
from app import schemas
import pytest



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

@pytest.mark.parametrize("email, password, status_code", [
    ("hello12@gmail.com", "1234", 200),
    ("hello12@gmail.com", "wrongpass", 403),
    ("wrongemail@gmail.com", "1234", 403)
])
def test_login_user_parametrized(test_user, client, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code



