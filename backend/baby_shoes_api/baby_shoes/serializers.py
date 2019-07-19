from rest_framework import serializers
from .models import BabyShoes


class BabyShoesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'story',
            'context_1',
            'question_1',
            'word_limit_1',
            'context_2',
            'question_2',
            'word_limit_2',
        )
        model = BabyShoes
