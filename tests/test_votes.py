import pytest

from app import models

@pytest.fixture()
def test_vote(test_user, session, test_posts):
    new_vote = models.Vote(post_id = test_posts[1].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 1})
    assert response.status_code == 201





def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json = {"post_id": test_posts[1].id, "direction": 1})
    assert response.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/vote/", json = {"post_id": test_posts[1].id, "direction": 0})
    assert response.status_code == 201

def test_delete_vote_non_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json = {"post_id": test_posts[1].id, "direction": 0})
    assert response.status_code == 404

def test_vote_on_post_non_exist(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json = {"post_id": 8000, "direction": 1})
    assert response.status_code == 404

def test_vote_unauth_user(client, test_posts):
    response = client.post("/vote/", json = {"post_id": test_posts[3].id, "direction": 1})
    assert response.status_code == 401