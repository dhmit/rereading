from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListBabyShoes.as_view()),
    path('add-response/', views.ListStudent.as_view()),
    path('<int:pk>/', views.DetailBabyShoes.as_view()),
]