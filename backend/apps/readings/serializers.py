"""
Serializers take models or other data structures and present them
in ways that can be transported across the backend/frontend divide, or
allow the frontend to suggest changes to the backend/database.
"""
from rest_framework import serializers

from .models import (
    StoryPrototype, QuestionPrototype, ContextPrototype, Student, StudentResponsePrototype
)


################################################################################
# Prototyping Serializers
# Serializers below were for the summer prototype
# and initial analysis prototyping
################################################################################
class StudentResponseSerializer(serializers.ModelSerializer):
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


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializes a student object and responses.
    """
    student_responses = StudentResponseSerializer(many=True)

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


class QuestionSerializer(serializers.ModelSerializer):
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


class ContextSerializer(serializers.ModelSerializer):
    """
    Serializes a Context object.
    """
    class Meta:
        model = ContextPrototype

        fields = (
            'id',
            'text',
        )


class StorySerializer(serializers.ModelSerializer):
    """
    Serializes a Story, including its questions and contexts.
    """
    contexts = serializers.StringRelatedField(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

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
    run_mean_reading_analysis_for_questions = serializers.ReadOnlyField()
    frequency_feelings = serializers.ReadOnlyField()
    context_vs_read_time = serializers.ReadOnlyField()
    question_sentiment_analysis = serializers.ReadOnlyField()
    compute_median_view_time = serializers.ReadOnlyField()

    def create(self, validated_data):
        """ We will not create new objects using this serializer """

    def update(self, instance, validated_data):
        """ We will not update data using this serializer """
