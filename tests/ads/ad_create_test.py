import pytest


@pytest.mark.django_db
def test_create_ad(client, user, category, user_token):
    expected_response = {
        "id": 1,
        "author": 1,
        "category": 1,
        "name": "test_ad_name",
        "price": 4000,
        "description": "",
        "is_published": False,
        "image": None
    }

    data = {
        "author": user.pk,
        "category": category.pk,
        "name": "test_ad_name",
        "price": 4000,
        "description": "",
        "is_published": False
    }

    response = client.post('/ad/create/', data, content_type='application/json',
                           HTTP_AUTHORIZATION="Bearer " + user_token)

    assert response.status_code == 201
    assert response.data == expected_response
