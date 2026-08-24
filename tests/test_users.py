
from app.main import app
from app import schemas
from .database import client, session





def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == 'Hello World from FastAPI!'
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email": "hello12@gmail.com", "password": "1234"})
    user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert user.email == "hello12@gmail.com"

