"""
These classes describe one way of entering into the web site.
"""

from rest_framework import generics
from .models import Story, Student
from .serializers import StorySerializer, StudentSerializer


# a ListCreateAPIView lets you view a list of objects or create a new one.
class ListStudent(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# RetrieveUpdateDestroyAPIView lets someone get a single object or update it
# or delete it.
class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ListStory(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer


class DetailStory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
