from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reviews.views import main_page_after_authentication_view
from reviews.api.api_views import LoginView, SurveyViewSet, SurveyView


router = DefaultRouter()
router.register(r'survey', SurveyViewSet, basename='all_survey')
router.register('survey/create', SurveyViewSet, basename='create_survey')


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('main_page/', main_page_after_authentication_view, name='main_page'),
    path('api/v1/', include(router.urls)),
    path('survey/change/<int:survey_id>/', SurveyView.as_view(), name='change_survey')
]
