import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_selection_create(client, user, ad, user_token):
    ads = AdFactory.create_batch(5)

    response = client.post('/selection/create/',
                           {"name": "test_selection", "author": user.pk, "ads": [ad.pk for ad in ads]},
                           HTTP_AUTHORIZATION="Bearer " + user_token)

    assert response.status_code == 201
    assert response.data == {"id": 1, "name": "test_selection", "author": user.pk, "ads": [ad.pk for ad in ads]}
