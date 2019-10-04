"""
Models for the Rereading app.
"""
from ast import literal_eval

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

    def __str__(self):
        return self.text


class Student(models.Model):
    """
    A user who reads stories and responds to questions.
    """
    name = models.TextField(default='')


class StudentResponse(models.Model):
    """
    The response of a student to a question given a context.

    TODO(msc): why are these not links to other models?
    """
    question = models.ForeignKey(
        Question,
        null=True,
        on_delete=models.SET_NULL,
        related_name='student_responses',
    )
    context = models.ForeignKey(
        Context,
        null=True,
        on_delete=models.SET_NULL,
        related_name='student_responses',
    )

    response = models.TextField(default='')
    views = models.TextField(default='')  # do not use me directly! see get_parsed_views()
    scroll_ups = models.IntegerField(default=0)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,  # if the Student is deleted, all her/his responses are too.
        related_name='student_responses',
    )

    def get_parsed_views(self):
        """
        Since views are stored as a TextField directly as the JSON representation
        of a list of floats, we need to convert this to a Python object in order
        to use it in our analyses.
        """

        return literal_eval(self.views)

    def get_question(self):

