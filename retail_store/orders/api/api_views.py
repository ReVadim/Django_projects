from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from Cart.api.serializers import OrderSerializer
from .serializers import ProductSerializer, CategorySerializer, UserSerializer, ContactSerializer, ShopSerializer, \
    ProductDetailSerializer, ProductParameterSerializer
from ..models import Product, Category, User, Contact, Shop, Order, ProductInfo, ProductParameter
from ..tasks import just_print


class ProductViewSet(ModelViewSet):
    """ Products ViewSet """

    throttle_scope = 'anon'
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):

        if self.action in ["create", "partial_update", 'destroy', "update"]:
            permissions = [IsAuthenticated]
        else:
            return []
        return [perm() for perm in permissions]


class CategoryViewSet(ModelViewSet):
    """ Category ViewSet """

    throttle_scope = 'anon'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class UserViewSet(ModelViewSet):
    """ User ViewSet """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class ContactViewSet(ModelViewSet):
    """ User detail information ViewSet """

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ShopView(ListAPIView):
    """ View store information """

    serializer_class = ShopSerializer
    queryset = Shop.objects.all()


class OrderViewSet(ModelViewSet):
    """ Order ViewSet """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):

        if self.action in ["create", "partial_update", 'destroy', "update"]:
            permissions = [IsAuthenticated]
        else:
            return []
        return [perm() for perm in permissions]


class ProductDetailViewSet(ModelViewSet):
    """ ProductDetailViewSet """

    serializer_class = ProductDetailSerializer
    queryset = ProductInfo.objects.all()


class ProductParameterViewSet(ModelViewSet):
    """ ProductParameterViewSet """

    serializer_class = ProductParameterSerializer
    queryset = ProductParameter.objects.all()
