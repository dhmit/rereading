"""
These classes describe one way of entering into the web site.
"""

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import StoryPrototype, Student
from .analysis import RereadingAnalysis
from .serializers import StorySerializer, StudentSerializer, AnalysisSerializer


@api_view(['GET'])
def reading_view(request, doc_id):
    """
    Send a document with its associated segments, questions, prompts, etc.
    to the frontend
    """
    # TODO(ra): implement me!


################################################################################
# Prototype views
# The API endpoints below were for the prototype from summer 2019
################################################################################
class ListStudent(generics.ListCreateAPIView):
    """ View a list of students of create a new one """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    """ Get a single Student or update/delete it """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ListStory(generics.ListCreateAPIView):
    """ Get a list of story objects """
    queryset = StoryPrototype.objects.all()
    serializer_class = StorySerializer


class DetailStory(generics.RetrieveUpdateDestroyAPIView):
    """ Get a single story object, or update/delete it """
    queryset = StoryPrototype.objects.all()
    serializer_class = StorySerializer


@api_view(['GET'])
def analysis(request):
    """
    Init a RereadingAnalysis, and serialize it to send to the frontend.
    """
    analysis_obj = RereadingAnalysis()
    serializer = AnalysisSerializer(instance=analysis_obj)
    return Response(serializer.data)
