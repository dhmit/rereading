"""
These classes describe one way of entering into the web site.
"""

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import StoryPrototype, Student, Document, StudentReadingData
from .analysis import RereadingAnalysis
from .serializers import (
    StoryPrototypeSerializer, StudentPrototypeSerializer, AnalysisSerializer,
    DocumentSerializer, StudentSerializer, DocumentAnalysisSerializer,
    StudentReadingDataSerializer, ReadingSerializer)


class ListDocument(generics.ListCreateAPIView):
    """View a list of documents or create a new one"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DetailDocument(generics.RetrieveUpdateDestroyAPIView):
    """Get a single document or update/delete it"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class Reading:
    def __init__(self, document, reading_data):
        self.document = document
        self.reading_data = reading_data


@api_view(['POST'])
def reading_view(request, pk):
    student_name = request.data.get('name')
    student = Student(name=student_name)
    student.save()
    doc = Document.objects.get(pk=pk)
    reading_data = StudentReadingData.objects.create(document=doc,
                                                     student=student)
    reading_data.save()
    reading = Reading(doc, reading_data)
    serializer = ReadingSerializer(reading)
    return Response(serializer.data)


@api_view(['GET'])
def document_analysis(request):
    """
    Init a DocumentAnalysis, and serialize it to send to the frontend.
    We are hardcoding the recitatif document for prototyping the DocumentAnalysis view
    """
    queryset = Document.objects.get(pk=1)
    serializer = DocumentAnalysisSerializer(queryset)
    return Response(serializer.data)


class ListStudent(generics.ListCreateAPIView):
    """View a list of students or create a new one"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DetailStudent(generics.RetrieveUpdateDestroyAPIView):
    """Get a single student's data or update/delete it"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class DetailReadingData(generics.RetrieveUpdateDestroyAPIView):
    """Get a single group of reading data or update/delete it"""
    queryset = StudentReadingData.objects.all()
    serializer_class = StudentReadingDataSerializer


class ListReadingData(generics.ListCreateAPIView):
    """View all instances of reading data"""
    queryset = StudentReadingData.objects.all()
    serializer_class = StudentReadingDataSerializer

################################################################################
# Prototype views
# The API endpoints below were for the prototype from summer 2019
################################################################################
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
    analysis_obj = RereadingAnalysis()
    serializer = AnalysisSerializer(instance=analysis_obj)
    return Response(serializer.data)
