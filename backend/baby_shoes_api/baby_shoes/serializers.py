from rest_framework import serializers
from .models import BabyShoes, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question

        fields = (
            'text',
            'word_limit'
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
