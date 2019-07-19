from django.db import models


# Create your models here.
class BabyShoes(models.Model):
    story = models.TextField()
    context_1 = models.TextField()
    question_1 = models.TextField()
    word_limit_1 = models.IntegerField()
    context_2 = models.TextField()
    question_2 = models.TextField()
    word_limit_2 = models.IntegerField()
