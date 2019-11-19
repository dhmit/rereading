"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers

from .models import (
    Document, Segment, Student, SegmentQuestion, SegmentContext, SegmentQuestionResponse,
    StudentReadingData, StudentSegmentData, DocumentQuestion, DocumentQuestionResponse,
)


class DocumentQuestionSerializer(serializers.ModelSerializer):
    """
    Serializes Document-level questions
    """

    class Meta:
        model = DocumentQuestion

        fields = (
            'id',
            'text',
            'is_overview_question',
        )


class DocumentQuestionResponseSerializer(serializers.ModelSerializer):
    """
    Serializes a Student's response to a given document-level question
    """
    id = serializers.ModelField(model_field=DocumentQuestionResponse()._meta.get_field('id'))

    class Meta:
        model = DocumentQuestionResponse

        fields = (
            'id',
            'response',
            'response_segment'
        )


class SegmentQuestionSerializer(serializers.ModelSerializer):
    """
    Serializes the questions that relate to a given segment
    """
    class Meta:
        model = SegmentQuestion

        fields = (
            'id',
            'text',
            'response_word_limit',
        )


class SegmentContextSerializer(serializers.ModelSerializer):
    """
    Serializes the contexts provided with a given segment
    """
    class Meta:
        model = SegmentContext

        fields = (
            'id',
            'text',
        )


class SegmentSerializer(serializers.ModelSerializer):
    """
    Serializes data related to a given segment of a document
    """
    questions = SegmentQuestionSerializer(many=True)
    contexts = SegmentContextSerializer(many=True)

    class Meta:
        model = Segment

        fields = (
            'id',
            'text',
            'sequence',
            'questions',
            'contexts',
        )


class SegmentQuestionResponseSerializer(serializers.ModelSerializer):
    """
    Serializes a response provided to a question from a segment
    """
    id = serializers.ModelField(model_field=SegmentQuestionResponse()._meta.get_field('id'))

    class Meta:
        model = SegmentQuestionResponse

        fields = (
            'id',
            'response',
        )


class StudentSegmentDataSerializer(serializers.ModelSerializer):
    """
    Serializes the data received from a user for a given segment
    """
    # To get the 'id' key to show up in validated_data in the create method
    id = serializers.ModelField(model_field=StudentSegmentData()._meta.get_field('id'))
    segment_responses = SegmentQuestionResponseSerializer(many=True)

    class Meta:
        model = StudentSegmentData

        fields = (
            'id',
            'scroll_data',
            'view_time',
            'is_rereading',
            'segment_responses',
        )


class StudentReadingDataSerializer(serializers.ModelSerializer):
    """
    Serializes the data received from all segments of a given document
    """

    segment_data = StudentSegmentDataSerializer(many=True)
    document_responses = DocumentQuestionResponseSerializer(many=True)
    reading_data_id = serializers.IntegerField(write_only=True)

    def update(self, instance, validated_data):
        """ Updates a StudentReadingData instance """

        # Separate out the responses
        segment_data = validated_data.pop("segment_data")
        document_responses = validated_data.pop("document_responses")
        reading_data = instance

        # Link each document response to the reading data
        for data in document_responses:
            document_question = DocumentQuestion.objects.get(id=data['id'])
            DocumentQuestionResponse.objects.create(
                student_reading_data=reading_data,
                question=document_question,
                response=data['response'],
                response_segment=data['response_segment'],
            )

        # Save student segment data
        for this_segment_data in segment_data:
            segment = Segment.objects.get(id=this_segment_data['id'])
            segment_data = StudentSegmentData.objects.create(
                segment=segment,
                reading_data=reading_data,
                scroll_data=this_segment_data['scroll_data'],
                view_time=this_segment_data['view_time'],
                is_rereading=this_segment_data['is_rereading']
            )

            # Save responses for this segment
            segment_question_responses = this_segment_data.pop('segment_responses')
            for response in segment_question_responses:
                question_id = response.pop('id')
                question = SegmentQuestion.objects.get(pk=question_id)
                SegmentQuestionResponse.objects.create(
                    student_segment_data=segment_data,
                    question=question,
                    **response,
                )

        return reading_data

    class Meta:
        model = StudentReadingData

        fields = (
            'id',
            'document_responses',
            'segment_data',
            'reading_data_id',
        )


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializes all data associated with the given student, i.e. reading data, responses, etc.
    """

    reading_data = StudentReadingDataSerializer(many=True)

    class Meta:
        model = Student

        fields = (
            'id',
            'reading_data',
        )


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializes Document metadata and associated segments
    """
    segments = SegmentSerializer(many=True, read_only=True)
    document_questions = serializers.SerializerMethodField(read_only=True)
    overview_questions = serializers.SerializerMethodField(read_only=True)

    def get_document_questions(self, obj):
        queryset = obj.questions.filter(is_overview_question=False)
        serializer = DocumentQuestionSerializer(queryset, many=True)
        return serializer.data

    def get_overview_questions(self, obj):
        queryset = obj.questions.filter(is_overview_question=True)
        serializer = DocumentQuestionSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Document

        fields = (
            'id',
            'title',
            'author',
            'document_questions',
            'overview_questions',
            'segments',
        )


class ReadingSerializer(serializers.Serializer):
    """ Serializer for main reading view """
    document = DocumentSerializer()
    reading_data = StudentReadingDataSerializer()

    def create(self, validated_data):
        """ We will not create new objects using this serializer """

    def update(self, instance, validated_data):
        """ We will not update data using this serializer """


class AnalysisSerializer(serializers.Serializer):
    """ Serializes analysis class """

    def create(self, validated_data):
        """ We will not create new objects using this serializer """

    def update(self, instance, validated_data):
        """ We will not update data using this serializer """
