"""
These classes describe one way of entering into the web site.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from .models import Student, Document, StudentReadingData, Writeup
from .analysis import RereadingAnalysis
from .serializers import (
    AnalysisSerializer,
    ReadingSerializer,
    StudentReadingDataSerializer,
    WriteupSerializer,
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
    """ API endpoint for updating student reading data as the student reads """
    data = request.data
    reading_data_id = data.get('reading_data_id')
    reading_data = StudentReadingData.objects.get(pk=reading_data_id)
    serializer = StudentReadingDataSerializer(instance=reading_data, data=data)
    is_valid = serializer.is_valid()

    if is_valid:
        serializer.save()
        return Response(serializer.data)
    else:
        # NOTE(ra) -- This is for debugging -- this really needs proper error handling
        print(serializer.errors)
        return Response({})



@api_view(['GET'])
def analysis(request):
    """
    Init a RereadingAnalysis, and serialize it to send to the frontend.
    """
    analysis_obj = RereadingAnalysis()
    serializer = AnalysisSerializer(instance=analysis_obj)
    return Response(serializer.data)


class ListStudentReadingData(generics.ListAPIView):
    """
    Lists all of the reading data acquired through the project
    """
    queryset = StudentReadingData.objects.all()
    serializer_class = StudentReadingDataSerializer


class WriteupListView(generics.ListAPIView):
    """
    Lists all of the student writeups
    """
    queryset = Writeup.objects.all()
    serializer_class = WriteupSerializer
