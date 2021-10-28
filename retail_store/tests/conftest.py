import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from model_bakery import baker
from orders.models import Shop


@pytest.fixture
def unauthorized_client():
    return APIClient()


@pytest.fixture()
def api_client(django_user_model):
    user = django_user_model.objects.create_user(username='user123', password='user123123', email='email@test.com')
    user_token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    return client


@pytest.fixture()
def api_partner(django_user_model):
    user = django_user_model.objects.create_user(
        username='user123',
        password='user123123',
        email='email@test.com',
        user_type='SHOP_MANAGER'
    )
    shop = Shop.objects.create(name="test_shop", url="tetsURL", manager=user)
    user_token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {user_token.key}')
    return client


@pytest.fixture
def admin_token(admin_user):
    token, _ = Token.objects.get_or_create(user=admin_user)
    return token.key


@pytest.fixture
def admin_client(admin_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token}')
    return client


@pytest.fixture
def shop_factory():

    def factory(**kwargs):
        return baker.make('Shop', **kwargs)
    return factory


@pytest.fixture
def order_factory():

    def factory(**kwargs):
        return baker.make('Order', **kwargs)
    return factory


@pytest.fixture
def product_factory():

    def factory(**kwargs):
        return baker.make('ProductInfo', **kwargs)
    return factory


@pytest.fixture
def category_factory():

    def factory(**kwargs):
        return baker.make('Category', **kwargs)
    return factory
