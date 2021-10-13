from django.urls import path, include, re_path
from .api_views import BalanceView, CreateBankAccountViewSet, HoldersView, AccountsView
from rest_framework.routers import DefaultRouter
from billing import views
from drf_spectacular.views import SpectacularAPIView


router = DefaultRouter()
router.register('create-account', CreateBankAccountViewSet, basename='create_account')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    re_path(r'^api/v1/balance/(?P<account_name>)$', BalanceView.as_view(), name='balance'),
    path('api/v1/holders/', HoldersView.as_view(), name='holders'),
    path('api/v1/accounts/', AccountsView.as_view(), name='accounts'),
    path('', views.payment_operation, name='payment'),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='shema')
]
