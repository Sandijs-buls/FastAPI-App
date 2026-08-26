import pytest
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostResponseWithVotes(**post)

    posts_list = list(map(validate, response.json()))
    assert len(posts_list) == len(test_posts)

    assert len(response.json()) == len(test_posts)

    assert response.status_code == 200


def test_unauth_user_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401
    

def test_unauth_user_get_one_posts(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/8989809")

    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    
    post = schemas.PostResponseWithVotes(**response.json())
    print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert post.title == title
    assert post.content == content

    assert post.owner_id == test_user['id'] 

def test_create_post_def_published(authorized_client, test_user, test_posts):
    response = authorized_client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})

    post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert post.title == "arbitrary title"
    assert post.content == "arbitrary content"
    assert post.published == True

    assert post.owner_id == test_user['id']

def test_unauth_user_create_post(client, test_user, test_posts):
    response = client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    assert response.status_code == 401

def test_unauth_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204 

def test_delete_post_non_exist(authorized_client, test_user):
    response = authorized_client.delete(f"/posts/800000")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    response = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)

    updated_post = schemas.PostResponse(**response.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert response.status_code == 200

def test_update_other_user_post(authorized_client, test_user,test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }

    response = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert response.status_code == 403

def test_unauth_user_update_post(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    response = authorized_client.put(f"/posts/800000", json = {"title": "updated title", "content": "updated content", "id": 800000})
    assert response.status_code == 404