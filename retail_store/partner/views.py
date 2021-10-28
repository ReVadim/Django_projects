from django.core.validators import URLValidator
from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from yaml import load as load_yaml, Loader
from distutils.util import strtobool
from requests import get
from rest_framework.response import Response

from Cart.api.serializers import OrderSerializer
from orders.api.serializers import ShopSerializer
from orders.models import Category, Shop, ProductInfo, Product, Parameter, ProductParameter, Order


class PartnerUpdate(APIView):
    """ Class for updating the price list from the supplier """

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'SHOP_MANAGER':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        url = request.data.get('url')
        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
                stream = get(url).content

                data = load_yaml(stream, Loader=Loader)

                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              price=item['price'],
                                                              price_retail=item['price_retail'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'All necessary arguments are not specified'})


class PartnerState(APIView):
    """ A class for working with the supplier status """

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.user_type != 'SHOP_MANAGER':
            return JsonResponse({'Status': False, 'Error': 'Shops only'}, status=403)

        shop = request.user.shop
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'SHOP_MANAGER':
            return JsonResponse({'Status': False, 'Error': 'Shops only'}, status=403)
        state = request.data.get('state')
        if state:
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
                return JsonResponse({'Status': True})
            except ValueError as error:
                return JsonResponse({'Status': False, 'Errors': str(error)})

        return JsonResponse({'Status': False, 'Errors': 'All necessary arguments are not specified'})


class PartnerOrders(APIView):
    """ A class for receiving orders by suppliers """

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.user_type != 'SHOP_MANAGER':
            return JsonResponse({'Status': False, 'Error': 'Shops only'}, status=403)

        order = Order.objects.filter(user=request.user)

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
