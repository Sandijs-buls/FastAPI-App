from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import SessionLocal
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#


Base.metadata.create_all(bind=engine)



def override_get_db():
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db



@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)



def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == 'Hello World from FastAPI!'
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email": "hello12@gmail.com", "password": "1234"})
    user = schemas.UserOut(**response.json())
    assert response.status_code == 201
    assert user.email == "hello12@gmail.com"

