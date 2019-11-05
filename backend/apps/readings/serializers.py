"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers

from .models import (
    Document, Segment, Student, SegmentQuestion, SegmentContext, SegmentQuestionResponse,
    StudentReadingData, StudentSegmentData, DocumentQuestion, DocumentQuestionResponse,
    StoryPrototype, QuestionPrototype, ContextPrototype, StudentResponsePrototype
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
        )


class DocumentQuestionResponseSerializer(serializers.ModelSerializer):
    """
    Serializes a Student's response to a given document-level question
    """

    class Meta:
        model = DocumentQuestionResponse

        fields = (
            'id',
            'text',
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

    class Meta:
        model = StudentSegmentData

        fields = (
            'id',
            'views',
            'scroll_ups',
        )


class StudentReadingDataSerializer(serializers.ModelSerializer):
    """
    Serializes the data received from all segments of a given document
    """

    segment_data = StudentSegmentDataSerializer(many=True)
    global_responses = DocumentQuestionResponseSerializer(many=True)

    class Meta:
        model = StudentReadingData

        fields = (
            'id',
            'segment_data',
            'global_responses',
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
    document_questions = DocumentQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Document

        fields = (
            'id',
            'title',
            'author',
            'document_questions',
            'segments',
        )


class DocumentAnalysisSerializer(serializers.Serializer):
    """
    Serializes Document analysis
    """
    total_word_count = serializers.ReadOnlyField()
    title_author = serializers.SerializerMethodField()

    @staticmethod
    def get_title_author(document):
        return str(document)

    def create(self, validated_data):
        """ We will not create new objects using this serializer """

    def update(self, instance, validated_data):
        """ We will not update data using this serializer """


################################################################################
# Prototyping Serializers
# Serializers below were for the summer prototype
# and initial analysis prototyping
################################################################################


class StudentResponsePrototypeSerializer(serializers.ModelSerializer):
    """
    A serializer makes it possible to view a database Django model
    on the web, such as React
    """
    class Meta:
        model = StudentResponsePrototype

        fields = (
            'id',
            'response',
            'views',
            'question',
            'context',
            'scroll_ups'
        )


class StudentPrototypeSerializer(serializers.ModelSerializer):
    """
    Serializes a student object and responses.
    """
    student_responses = StudentResponsePrototypeSerializer(many=True)

    def create(self, validated_data):
        """
        Create a Student object and its responses

        :param validated_data: dict
        :return: Student
        """
        responses_data = validated_data.pop('student_responses')
        student = Student.objects.create(**validated_data)
        for response_data in responses_data:
            StudentResponsePrototype.objects.create(student=student, **response_data)

        return student

    class Meta:
        model = Student

        fields = (
            'id',
            # 'story',
            'student_responses',
        )


class QuestionPrototypeSerializer(serializers.ModelSerializer):
    """
    Serializes a Question object.
    """
    class Meta:
        model = QuestionPrototype

        fields = (
            'id',
            'text',
            'word_limit'
        )


class ContextPrototypeSerializer(serializers.ModelSerializer):
    """
    Serializes a Context object.
    """
    class Meta:
        model = ContextPrototype

        fields = (
            'id',
            'text',
        )


class StoryPrototypeSerializer(serializers.ModelSerializer):
    """
    Serializes a Story, including its questions and contexts.
    """
    contexts = serializers.StringRelatedField(many=True, read_only=True)
    questions = QuestionPrototypeSerializer(many=True, read_only=True)

    class Meta:
        model = StoryPrototype
        fields = (
            'id',
            'story_text',
            'contexts',
            'questions',
        )


class AnalysisSerializer(serializers.Serializer):
    """ Serializes analysis class """
    total_view_time = serializers.ReadOnlyField()
    all_responses = serializers.ReadOnlyField()
    run_mean_reading_analysis_for_questions = serializers.ReadOnlyField()
    frequency_feelings = serializers.ReadOnlyField()
    context_vs_read_time = serializers.ReadOnlyField()
    question_sentiment_analysis = serializers.ReadOnlyField()
    compute_median_view_time = serializers.ReadOnlyField()
    mean_view_time_comparison = serializers.ReadOnlyField()
    compute_mean_response_length = serializers.ReadOnlyField()
    percent_using_relevant_words_by_context_and_question = serializers.ReadOnlyField()

    def create(self, validated_data):
        """ We will not create new objects using this serializer """

    def update(self, instance, validated_data):
        """ We will not update data using this serializer """
