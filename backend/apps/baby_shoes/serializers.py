from rest_framework import serializers
from .models import BabyShoes, Question, Context, Student, StudentResponse


class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResponse

        fields = (
            'response',
            'views',
            'question',
            'context',
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
            'story',
            'student_responses',
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question

        fields = (
            'text',
            'word_limit'
        )


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context

        fields = (
            'text',
        )


class BabyShoesSerializer(serializers.ModelSerializer):
    contexts = serializers.StringRelatedField(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = BabyShoes
        fields = (
            'id',
            'story',
            'contexts',
            'questions',
        )
