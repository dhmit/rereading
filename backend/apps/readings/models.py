"""
Models for the Rereading app.
"""
from django.db import models


class Story(models.Model):
    """
    A single story with its text.
    """
    story_text = models.TextField()

    def __str___(self):
        return self.story_text


class Context(models.Model):
    """
    The Context in which a story is read.
    """
    text = models.TextField()
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='contexts',
    )

    def __str__(self):
        return self.text


class Question(models.Model):
    """
    A question about a Story.
    """
    text = models.TextField()
    word_limit = models.IntegerField()
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='questions',
    )


class Student(models.Model):
    """
    A user who reads stories and responds to questions.
    """
    story = models.TextField(default='')


class StudentResponse(models.Model):
    """
    The response of a student to a question given a context.

    TODO(msc): why are these not links to other models?
    """
    question = models.TextField(default='')
    context = models.TextField(default='')
    response = models.TextField(default='')
    views = models.TextField(default='')
    scroll_ups = models.IntegerField(default=0)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,  # if the Student is deleted, all her/his responses are too.
        related_name='student_responses',
    )
