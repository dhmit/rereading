from django.shortcuts import render
from rest_framework import generics
from .models import Story, Student
from .serializers import StorySerializer, StudentSerializer


class ListStudent(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Create your views here.
class ListStory(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class DetailStory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
