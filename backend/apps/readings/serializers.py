from rest_framework import serializers
from .models import Story, Question, Context, Student, StudentResponse


class StudentResponseSerializer(serializers.ModelSerializer):
    """
    A serializer makes it possible to view a database Django model
    on the web, such as React
    """
    class Meta:
        model = StudentResponse

        fields = (
            'id',
            'response',
            'views',
            'question',
            'context',
            'scroll_ups'
        )


class StudentSerializer(serializers.ModelSerializer):
    student_responses = StudentResponseSerializer(many=True)

    def create(self, validated_data):
        responses_data = validated_data.pop('student_responses')
        student = Student.objects.create(**validated_data)
        for response_data in responses_data:
            StudentResponse.objects.create(student=student, **response_data)

        return student

    class Meta:
        model = Student

        fields = (
            'id',
            'story',
            'student_responses',
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question

        fields = (
            'id',
            'text',
            'word_limit'
        )


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context

        fields = (
            'id',
            'text',
        )


class StorySerializer(serializers.ModelSerializer):
    contexts = serializers.StringRelatedField(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = (
            'id',
            'story',
            'contexts',
            'questions',
        )
