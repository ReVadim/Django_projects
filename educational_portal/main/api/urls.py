from django.urls import path, include
from rest_framework.routers import DefaultRouter

from courses.views import new_comment
from main.api.api_views import CoursesViewSet, MaterialViewSet, ProgramViewSet, CourseCommentViewSet, \
    CourseAssessmentViewSet, add_comment, show_comment, delete_comment


router = DefaultRouter()
router.register('course/all', CoursesViewSet, basename='courses')
router.register('materials/all', MaterialViewSet, basename='materials')
router.register('programs/all', ProgramViewSet, basename='programs')
router.register('course/comments/all', CourseCommentViewSet, basename='comments')
router.register('course/assessments/all', CourseAssessmentViewSet, basename='course_assessment')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('course/comments/<int:course_pk>/', show_comment, name='all_comments'),
    path('comment/new/<int:course_pk>/', add_comment, name='new_comment'),
    path('comment/delete/<int:comment_pk>', delete_comment, name='del_comment'),
]
