from django.shortcuts import render
from rest_framework import generics
from .models import BabyShoes, Student
from .serializers import BabyShoesSerializer, StudentSerializer


class ListStudent(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Create your views here.
class ListBabyShoes(generics.ListCreateAPIView):
    queryset = BabyShoes.objects.all()
    serializer_class = BabyShoesSerializer


class DetailBabyShoes(generics.RetrieveUpdateDestroyAPIView):
    queryset = BabyShoes.objects.all()
    serializer_class = BabyShoesSerializer
