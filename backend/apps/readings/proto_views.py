"""
Prototype views
The API endpoints below were for the prototype from summer 2019
"""

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import StoryPrototype, Student
from .proto_analysis import PrototypeRereadingAnalysis
from .proto_serializers import (
    StoryPrototypeSerializer, StudentPrototypeSerializer, PrototypeAnalysisSerializer
)


class ListStudentPrototype(generics.ListCreateAPIView):
    """ View a list of students of create a new one """
    queryset = Student.objects.all()
    serializer_class = StudentPrototypeSerializer


class DetailStudentPrototype(generics.RetrieveUpdateDestroyAPIView):
    """ Get a single Student or update/delete it """
    queryset = Student.objects.all()
    serializer_class = StudentPrototypeSerializer


class ListStoryPrototype(generics.ListCreateAPIView):
    """ Get a list of story objects """
    queryset = StoryPrototype.objects.all()
    serializer_class = StoryPrototypeSerializer


class DetailStoryPrototype(generics.RetrieveUpdateDestroyAPIView):
    """ Get a single story object, or update/delete it """
    queryset = StoryPrototype.objects.all()
    serializer_class = StoryPrototypeSerializer


@api_view(['GET'])
def analysis(request):
    """
    Init a RereadingAnalysis, and serialize it to send to the frontend.
    """
    analysis_obj = PrototypeRereadingAnalysis()
    serializer = PrototypeAnalysisSerializer(instance=analysis_obj)
    return Response(serializer.data)
