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
from django.urls import path
from django.conf.urls import url

from apps.common import render_react_view
from apps.readings import views as readings_views


urlpatterns = [
    # Django admin page
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', readings_views.ListStory.as_view()),
    path('api/add-response/', readings_views.ListStudent.as_view()),
    path('api/<int:pk>/', readings_views.DetailStory.as_view()),
    path('api/analysis/', readings_views.analysis),

    # React views
    url('student/', render_react_view, {'component_name': 'StudentView'}),
    url('instructor/', render_react_view, {'component_name': 'InstructorView'}),
]
