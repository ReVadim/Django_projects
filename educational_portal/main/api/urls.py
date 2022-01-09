from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.api.api_views import CoursesViewSet, MaterialViewSet, ProgramViewSet


router = DefaultRouter()
router.register('course/all', CoursesViewSet, basename='courses')
router.register('materials/all', MaterialViewSet, basename='materials')
router.register('programs/all', ProgramViewSet, basename='materials')


urlpatterns = [
    path('api/v1/', include(router.urls)),
]
