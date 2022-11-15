import pytest

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client, ad, user_token):

    response = client.get(f'/ad/{ad.pk}/', HTTP_AUTHORIZATION="Bearer " + user_token)

    assert response.status_code == 200
    assert response.data == AdListSerializer(ad).data
