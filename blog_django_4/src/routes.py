from django.urls import path, include


urlpatterns = [
    path('', include('src.blog.urls')),
]
