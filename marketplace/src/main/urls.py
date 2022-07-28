from django.urls import path

from .views import index, other_page, MarketplaceLoginView


app_name = 'src.main'
urlpatterns = [
    path('accounts/login/', MarketplaceLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
