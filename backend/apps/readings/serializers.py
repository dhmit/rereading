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

    class Meta:
        model = StudentSegmentData

        fields = (
            'id',
            'scroll_data',
            'view_time',
            'is_rereading',
        )


class StudentReadingDataSerializer(serializers.ModelSerializer):
    """
    Serializes the data received from all segments of a given document
    """

    segment_data = StudentSegmentDataSerializer(many=True)
    # document_responses = DocumentQuestionResponseSerializer(many=True)
    segment_responses = SegmentQuestionResponseSerializer(many=True)
    reading_data_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        """
        Creates a new reading data instance
        :param validated_data:
        :return:
        """
        # Separate out the responses
        segment_question_data = validated_data.pop("segment_responses")
        seg_data = validated_data.pop("segment_data")

        reading_data_id = validated_data.pop("reading_data_id")

        # Create a new reading data instance if one doesn't exist already
        # with the primary key. It returns a tuple with the StudentReadingData
        # object and a boolean about whether it created it or not
        reading_data = StudentReadingData.objects.get(pk=reading_data_id)

        # TODO: Use this when we answer collect the document question responses
        # print(reading_data)
        # Link each global response to the reading data
        # for data in global_data:
        #     document_question = DocumentQuestion.objects.get(id=data['id'])
        #     DocumentQuestionResponse.objects.create(
        #         student_reading_data=reading_data,
        #         question=document_question,
        #         response=data['response']
        #     )

        for data in segment_question_data:
            segment_question = SegmentQuestion.objects.get(id=data['id'])
            SegmentQuestionResponse.objects.create(
                question=segment_question,
                student_reading_data=reading_data,
                response=data['response'],
            )

        # Link each segment response to the reading data

        for data in seg_data:
            segment = Segment.objects.get(id=data['id'])
            StudentSegmentData.objects.create(
                segment=segment,
                reading_data=reading_data,
                scroll_data=data['scroll_data'],
                view_time=data['view_time'],
                is_rereading=data['is_rereading']
            )
        return reading_data

    class Meta:
        model = StudentReadingData

        fields = (
            'id',
            # 'document_responses',
            'segment_responses',
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
    questions = DocumentQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Document

        fields = (
            'id',
            'title',
            'author',
            'questions',
            'segments',
        )


class ReadingSerializer(serializers.Serializer):
    document = DocumentSerializer()
    reading_data = StudentReadingDataSerializer()

    def create(self, validated_data):
        """ We will not create new objects using this serializer """

    def update(self, instance, validated_data):
        """ We will not update data using this serializer """


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
    compute_mean_response_length = serializers.ReadOnlyField()
    percent_using_relevant_words_by_context_and_question = serializers.ReadOnlyField()

    def create(self, validated_data):
        """ We will not create new objects using this serializer """

    def update(self, instance, validated_data):
        """ We will not update data using this serializer """
