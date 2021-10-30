"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path

from publish.views import view_post
from main.views import home, verify


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)', view_post, name='view_post'),
    url(r'^$', home, name='home'),
    url(r'^verify/(?P<uuid>[a-z0-9\-]+)/', verify, name='verify'),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)', view_post, name='view_post'),
]
