import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_not_partner(api_client):
    url = reverse('partner-state')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_partner(api_partner):
    url = reverse('partner-state')
    resp = api_partner.get(url)
    assert resp.status_code == HTTP_200_OK
