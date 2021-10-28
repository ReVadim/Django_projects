from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from Cart.api.api_views import CartView
from orders.api.api_views import ProductViewSet, CategoryViewSet, ContactViewSet, ShopView, OrderViewSet, \
    ProductDetailViewSet, ProductParameterViewSet
from orders.views import LoginAccount, ConfirmAccount, RegisterAccount, LoginView, RegistrationView, AccountDetails
from partner.views import PartnerState, PartnerOrders, PartnerUpdate

router = DefaultRouter()
router.register('product/categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('product/details', ProductDetailViewSet, basename='product-detail')
router.register('product/parameter', ProductParameterViewSet, basename='product-parameter')
router.register('users/contact', ContactViewSet, basename='user-contact-info')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('api/v1/retail/shops/', ShopView.as_view(), name='shops'),
    path('api/v1/cart/', CartView.as_view(), name='cart'),
    path('api/v1/', include(router.urls)),
    path('user/login/', LoginAccount.as_view(), name='user-login'),
    path('user/register/', RegisterAccount.as_view(), name='user-register'),
    path('user/register/confirm/', ConfirmAccount.as_view(), name='user-register-confirm'),
    path('user/detail/', AccountDetails.as_view(), name='account-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('partner/state/', PartnerState.as_view(), name='partner-state'),
    path('partner/order/', PartnerOrders.as_view(), name='partner-orders'),
    path('partner/update/', PartnerUpdate.as_view(), name='partner-update'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
