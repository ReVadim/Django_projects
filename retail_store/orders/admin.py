from django.contrib import admin
from .models import User, Product, Parameter, Order, OrderItem, Shop, Category, ProductInfo, ProductParameter, Contact

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Parameter)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(ProductInfo)
admin.site.register(ProductParameter)
admin.site.register(Contact)
