import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from ...orders.models import User
from ...orders.views import AccountDetails


factory = APIRequestFactory()


@pytest.mark.django_db
def test_get_order(api_client, order_factory):
    url = reverse('orders-list')
    order_factory(_quantity=7)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json['results']) == 7


@pytest.mark.django_db
def test_get_shops(api_client, shop_factory):
    url = reverse('shops')
    shop_factory(_quantity=2)
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json['results']) == 2


@pytest.mark.django_db
def test_create_category(api_client):
    url = reverse('category-list')
    data = {"name": "test_category"}
    resp = api_client.post(url, data=data, format='json')
    assert resp.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_create_product(api_client):
    url = reverse('product-list')
    url1 = reverse('category-list')
    category = api_client.post(url1, data={"name": "category"}, format='json')
    assert category.status_code == HTTP_201_CREATED
    data = {"name": "test_product", "category": 1}
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_create_product_info(api_client, shop_factory):
    url_category = reverse('category-list')
    shop_factory(_quantity=1)
    api_client.post(url_category, data={"name": "category"}, format='json')
    url_product = reverse('product-list')
    resp = api_client.post(url_product, data={"name": "test_product", "category": 1}, format='json')
    assert resp.status_code == HTTP_201_CREATED
    url = reverse('product-detail-list')
    data = {"product": 1, "shop": 1, "quantity": 7, "description": "test_text", "price": 9.99, "price_retail": 20.99}
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == HTTP_201_CREATED
    resp_json = response.json()
    assert resp_json["price"] == '9.99'


def test_login_account():
    user = User.objects.get(name='Ann')
    view = AccountDetails.as_view()
    request = factory.post('/user/login/', {'email': 'Sam@email.com', 'password': 'SamPassword'}, format='json')
    force_authenticate(request, user=user)
    response = view(request)
    assert response
