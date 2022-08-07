from django.urls import path

from .views import (
    index,
    other_page,
    MarketplaceLoginView,
    profile, MarketplaceLogoutView,
    RegisterDoneView, RegisterUserView,
    ChangeUserInfoView, MarketplacePasswordChangeView,
    user_activate, DeleteUserView, by_rubric, detail,
)


app_name = 'src.main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/login/', MarketplaceLoginView.as_view(), name='login'),
    path('accounts/logout/', MarketplaceLogoutView.as_view(), name='logout'),
    path('accounts/password/change', MarketplacePasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
