"""
This file controls the administrative interface for the
Rereading project's "readings" app.
"""

from django.contrib import admin
from .models import (
    StoryPrototype, ContextPrototype, QuestionPrototype, Student, StudentResponsePrototype
)


class StudentResponseInline(admin.TabularInline):
    model = StudentResponsePrototype
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    model = Student
    inlines = [StudentResponseInline]


class QuestionInline(admin.TabularInline):
    model = QuestionPrototype
    extra = 1


class ContextInline(admin.TabularInline):
    model = ContextPrototype
    extra = 1


class StoryAdmin(admin.ModelAdmin):
    model = StoryPrototype
    inlines = [ContextInline, QuestionInline]


admin.site.register(StoryPrototype, StoryAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentResponsePrototype)
admin.site.register(ContextPrototype)
admin.site.register(QuestionPrototype)
