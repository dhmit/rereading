"""
This file controls the administrative interface for the
Rereading project's "readings" app.
"""

from django.contrib import admin
from .models import (
    Student,
    Document,
    Segment,
    SegmentQuestion,
    SegmentQuestionResponse,
    DocumentQuestion,
    DocumentQuestionResponse,
    StudentSegmentData,
    StudentReadingData,
    Writeup,
)


################################################################################
# Document admin view
################################################################################
class SegmentInline(admin.TabularInline):
    model = Segment
    extra = 1


class DocumentQuestionInline(admin.TabularInline):
    model = DocumentQuestion
    extra = 1


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    inlines = [SegmentInline, DocumentQuestionInline]


################################################################################
# Segment admin view
################################################################################
class SegmentQuestionInline(admin.TabularInline):
    model = SegmentQuestion
    extra = 1


class SegmentAdmin(admin.ModelAdmin):
    model = Segment
    inlines = [SegmentQuestionInline]


################################################################################
# Questions admin views
################################################################################
class SegmentQuestionResponseInline(admin.TabularInline):
    model = SegmentQuestionResponse


class DocumentQuestionResponseInline(admin.TabularInline):
    model = DocumentQuestionResponse


class DocumentQuestionAdmin(admin.ModelAdmin):
    model = DocumentQuestion
    inlines = [DocumentQuestionResponseInline]


class SegmentQuestionAdmin(admin.ModelAdmin):
    model = SegmentQuestionResponse
    list_display = ('segment', 'sequence', 'text',)
    inlines = [SegmentQuestionResponseInline]


################################################################################
# Student data admin view
################################################################################
class StudentSegmentDataInline(admin.TabularInline):
    model = StudentSegmentData


class StudentReadingDataAdmin(admin.ModelAdmin):
    model = StudentReadingData
    inlines = [StudentSegmentDataInline]


class StudentSegmentDataAdmin(admin.ModelAdmin):
    model = StudentSegmentData
    inlines = [SegmentQuestionResponseInline]


admin.site.register(Student)
admin.site.register(Writeup)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(StudentReadingData, StudentReadingDataAdmin)
admin.site.register(StudentSegmentData, StudentSegmentDataAdmin)
admin.site.register(SegmentQuestion, SegmentQuestionAdmin)
admin.site.register(DocumentQuestion, DocumentQuestionAdmin)
