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
    SegmentContext,
)


################################################################################
# Document admin view
################################################################################
class SegmentInline(admin.TabularInline):
    model = Segment
    extra = 1


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    inlines = [SegmentInline]


################################################################################
# Segment admin view
################################################################################
class SegmentContextInline(admin.TabularInline):
    model = SegmentContext
    extra = 1


class SegmentQuestionInline(admin.TabularInline):
    model = SegmentQuestion
    extra = 1


class SegmentAdmin(admin.ModelAdmin):
    model = Segment
    inlines = [SegmentContextInline, SegmentQuestionInline]


admin.site.register(Document, DocumentAdmin)
admin.site.register(Student)
admin.site.register(Segment, SegmentAdmin)

