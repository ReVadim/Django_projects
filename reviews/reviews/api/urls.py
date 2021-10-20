from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reviews.views import main_page_after_authentication_view
from drf_spectacular.views import SpectacularAPIView
from reviews.api.api_views import LoginView, SurveyViewSet, SurveyView, QuestionViewSet, QuestionView, AnswerView


router = DefaultRouter()
router.register(r'survey', SurveyViewSet, basename='all_survey')
router.register('survey/create', SurveyViewSet, basename='create_survey')
router.register('question/create', QuestionViewSet, basename='create_question')


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('main_page/', main_page_after_authentication_view, name='main_page'),
    path('api/v1/', include(router.urls)),
    path('survey/change/<int:survey_id>/', SurveyView.as_view(), name='change_survey'),
    path('api/v1/question/change/<int:question_id>/', QuestionView.as_view(), name='change_question'),
    path('api/v1/answer/view/<int:user_id>/', AnswerView.as_view(), name='view_answer'),
    path('api/v1/answer/create', AnswerView.as_view(), name='create_answer'),
    path('api/v1/answer/change/<int:answer_id>/', AnswerView.as_view(), name='change_answer'),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema')
]
