from django.db import models


# Create your models here.
class Story(models.Model):
    story = models.TextField()

    def __str___(self):
        return self.story


class Context(models.Model):

    text = models.TextField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='contexts')

    def __str__(self):
        return self.text


class Question(models.Model):

    text = models.TextField()
    word_limit = models.IntegerField()
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='questions')


class Student(models.Model):

    story= models.TextField(default='')


class StudentResponse(models.Model):

    question = models.TextField(default='')
    context = models.TextField(default='')
    response = models.TextField(default='')
    views = models.IntegerField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_responses')


