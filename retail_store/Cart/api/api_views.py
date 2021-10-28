from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from selenium.webdriver.remote.utils import load_json
from rest_framework.response import Response
from Cart.api.serializers import OrderItemSerializer
from orders.models import Order, OrderItem


class CartView(APIView):
    """ A class for working with the user's shopping cart """

    throttle_scope = 'anon'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        queryset = OrderItem.objects\
            .select_related("order", "product_info")\
            .prefetch_related("order__user").filter(order__user=request.user)
        total_price = 0
        for item in queryset:
            total_price += item.product_info.quantity * item.product_info.price_retail

        serializer = OrderItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            cart, _ = Order.objects.get_or_create(user_id=request.user.id, state='cart')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=cart.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Objects deleted': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'All necessary arguments are not specified'})

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Invalid request format'})
            else:
                cart, _ = Order.objects.get_or_create(user_id=request.user.id, state='cart')
                objects_updated = 0
                for order_item in items_dict:
                    if type(order_item['id']) == int and type(order_item['quantity']) == int:
                        objects_updated += OrderItem.objects.filter(order_id=cart.id, id=order_item['id']).update(
                            quantity=order_item['quantity'])

                return JsonResponse({'Status': True, 'Objects updated': objects_updated})
        return JsonResponse({'Status': False, 'Errors': 'All necessary arguments are not specified'})
