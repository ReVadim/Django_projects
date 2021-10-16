from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reviews.views import main_page_after_authentication_view
from reviews.api.api_views import LoginView, SurveyViewSet


router = DefaultRouter()
router.register('survey/create/', SurveyViewSet, basename='create_survey')
router.register('survey/update/<int: survey_id>/', SurveyViewSet, basename='update_survey')
router.register('survey/delete/<int: survey_id>/', SurveyViewSet, basename='delete_survey')


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('main_page/', main_page_after_authentication_view, name='main_page'),
    path('api/v1/', include(router.urls)),
]
