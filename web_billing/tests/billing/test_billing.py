import pytest
from django.urls import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_200_OK


@pytest.mark.django_db
def test_create_new_holder(new_user):
    """ new holder creation """
    url = reverse('holders')
    resp = new_user.get(url)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create_bank_account(api_client, bank_account_factory):
    """ Checking the creation of a bank account """
    bank_account_factory(_quantity=1)
    url = reverse('create_account-list')
    resp = api_client.get(url)
    assert resp.status_code == HTTP_401_UNAUTHORIZED
    resp_json = resp.json()
    assert len(resp_json) == 1
