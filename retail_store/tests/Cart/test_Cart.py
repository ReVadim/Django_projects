import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED


URL = reverse('cart')


@pytest.mark.django_db
def test_get_order_item(api_client):
    resp = api_client.get(URL)
    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_get_order_item(unauthorized_client):
    resp = unauthorized_client.get(URL)
    assert resp.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_order_item(api_client, order_factory, shop_factory):
    order_factory(_quantity=2)
    shop_factory(_quantity=2)
    url = reverse('product-list')
    url1 = reverse('category-list')
    category = api_client.post(url1, data={"name": "category"}, format='json')
    assert category.status_code == HTTP_201_CREATED
    data = {"name": "test_product", "category": 1}
    api_client.post(url, data=data, format='json')
    url_2 = reverse('product-detail-list')
    data1 = {"product": 1, "shop": 1, "quantity": 7, "description": "test_text", "price": 9.99, "price_retail": 20.99}
    response = api_client.post(url_2, data=data1, format='json')
    assert response.status_code == HTTP_201_CREATED
    data2 = {"order": 1, "product": 1, "shop": 1, "quantity": 2, "product_info": 1}
    resp = api_client.post(URL, data2, format='json')
    assert resp.status_code == HTTP_200_OK
