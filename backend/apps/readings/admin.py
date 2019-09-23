"""
This file controls the administrative interface for the
Rereading project's "readings" app.
"""

from django.contrib import admin
from .models import Story, Context, Question, Student, StudentResponse


class StudentResponseInline(admin.TabularInline):
    model = StudentResponse
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    model = Student
    inlines = [StudentResponseInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class ContextInline(admin.TabularInline):
    model = Context
    extra = 1


class StoryAdmin(admin.ModelAdmin):
    model = Story
    inlines = [ContextInline, QuestionInline]


admin.site.register(Story, StoryAdmin)
admin.site.register(Student, StudentAdmin)
