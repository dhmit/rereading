from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListStory.as_view()),
    path('add-response/', views.ListStudent.as_view()),
    path('<int:pk>/', views.DetailStory.as_view()),
]