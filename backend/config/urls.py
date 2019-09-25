"""
Rereading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL configuration
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView


from apps.readings import views as readings_views


class SinglePageApp(TemplateView):
    template_name = 'index.html'


urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', readings_views.ListStory.as_view()),
    path('api/add-response/', readings_views.ListStudent.as_view()),
    path('api/<int:pk>/', readings_views.DetailStory.as_view()),

    url('', SinglePageApp.as_view()),

    # capture all other urls, so other routes can take over
    re_path(r'^(?:.*)/?$', SinglePageApp.as_view()),
]
