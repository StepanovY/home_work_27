import pytest


@pytest.fixture
@pytest.mark.dgango_db
def user_token(client, django_user_model):
    username = 'username'
    password = 'test_password'

    django_user_model.objects.create_user(
        username=username, password=password, role='admin'
    )

    response = client.post(
        '/user/token/',
        {"username": username, "password": password},
        content_type='application/json'
    )

    return response.data['access']
