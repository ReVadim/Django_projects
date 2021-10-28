from rest_framework import serializers

from orders.api.serializers import UserSerializer, ProductSerializer, ShopSerializer
from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    """ Order serializer """

    user = UserSerializer

    class Meta:
        model = Order
        fields = ['user', 'date', 'order_state']


class OrderItemSerializer(serializers.ModelSerializer):
    """ OrderItemSerializer """

    order = OrderSerializer
    product = ProductSerializer
    shop = ShopSerializer

    class Meta:
        model = OrderItem
        fields = '__all__'
