"""
These classes describe one way of entering into the web site.
"""

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Student, Document, StudentReadingData
from .analysis import RereadingAnalysis
from .serializers import (
    AnalysisSerializer,
    ReadingSerializer,
    StudentReadingDataSerializer,
    StudentSerializer,
)


class Reading:
    """ Class to aggregate all of the models we need to serialize for the reading view """
    def __init__(self, document, reading_data):
        self.document = document
        self.reading_data = reading_data


@api_view(['POST'])
def reading_view(request, pk):
    """ Primary API endpoint for the reading view -- called with the student's name
        from the view (to be written) where we collect that
    """
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


@api_view(['POST'])
def add_response(request):
    data = request.data
    serializer = StudentReadingDataSerializer(data=data)
    serializer.is_valid()
    serializer.save()
    return Response(serializer.data)


@api_view(['GET'])
def analysis(request):
    """
    Init a RereadingAnalysis, and serialize it to send to the frontend.
    """
    analysis_obj = RereadingAnalysis()
    serializer = AnalysisSerializer(instance=analysis_obj)
    return Response(serializer.data)

