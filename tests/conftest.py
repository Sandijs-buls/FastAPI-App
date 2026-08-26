#Fixtures to be moved here

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
from app.oauth2 import create_access_token
from app import models
from alembic import command



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    #command.upgrade("head")
    #command.downgrade("base")


@pytest.fixture()
def test_user2(client):
    user_data = {"email" : "hello123@gmail.com", "password" : "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user(client):
    user_data = {"email" : "hello12@gmail.com", "password" : "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user




@pytest.fixture()
def test_posts(test_user, test_user2, session):
    posts_data = [

        {"title": "test title 1", "content": "test content 1", "owner_id": test_user['id']},
        {"title": "test title 2", "content": "test content 2", "owner_id": test_user['id']},
        {"title": "test title 3", "content": "test content 3", "owner_id": test_user['id']},
        {"title": "test title 4", "content": "test content 4", "owner_id": test_user2['id']}

    ]

    def create_post_model(post):
        return models.Post(**post)
    postmap = map(create_post_model, posts_data)  # This will map the function to each element in the list

    post_list = list(postmap)  # This will create a list of Post models

    session.add_all(post_list)
    session.commit()

    posts = session.query(models.Post).all()
    return posts


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"

    }

    return client