import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework.authtoken.models import Token

from billing.models import BankAccount, Holder


@pytest.fixture
def bank_account_factory():

    def factory(**kwargs):
        return baker.make('BankAccount', **kwargs)
    return factory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_factory():

    def factory(**kwargs):
        return baker.make('Holder', **kwargs)
    return factory


@pytest.fixture
def new_user():
    user = Holder.objects.create(username='test_name', email='test@email.com', password='test_pass')
    token = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client
