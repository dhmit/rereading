from rest_framework import serializers
from .models import BabyShoes, Question, Context, Student, StudentResponse


class StudentResponseSerializer(serializers.ModelSerializer):
    responses = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = StudentResponse

        fields = (
            'response',
            'views',
        )


class StudentSerializer(serializers.ModelSerializer):
    answers = StudentResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Student

        fields = (
            'answers',
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
