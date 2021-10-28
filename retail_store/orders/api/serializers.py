from rest_framework import serializers

from ..models import Product, Category, Contact, User, Shop, ProductInfo, Parameter, ProductParameter


class ProductSerializer(serializers.ModelSerializer):
    """ Products serializer """

    name = serializers.CharField(required=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """ Category serializer """

    name = serializers.CharField(required=True)

    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    """ User contact information serializer """

    class Meta:
        model = User
        fields = ['username', 'user_type', 'email']


class ContactSerializer(serializers.ModelSerializer):
    """ full information about the user serializer """

    user = UserSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    """ Shop serializer """
    name = serializers.CharField(required=True)
    url = serializers.URLField()
    manager = UserSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = ['name', 'url', 'manager']


class ProductDetailSerializer(serializers.ModelSerializer):
    """ Product information serializer """
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects)
    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'description', 'quantity', 'price', 'price_retail']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = "__all__"


class ProductParameterSerializer(serializers.ModelSerializer):
    """ ProductParameter serializer """
    product_info = ProductDetailSerializer
    parameter = ParameterSerializer

    class Meta:
        model = ProductParameter
        fields = "__all__"
