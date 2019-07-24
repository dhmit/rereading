from django.contrib import admin
from .models import BabyShoes, Context, Question, Student

# Register your models here.
# admin.site.register(BabyShoes)
# admin.site.register(Context)


class StudentAdmin(admin.ModelAdmin):
    model = Student


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class ContextInline(admin.TabularInline):
    model = Context
    extra = 1


class BabyShoesAdmin(admin.ModelAdmin):
    model = BabyShoes
    inlines = [ContextInline, QuestionInline]


admin.site.register(BabyShoes, BabyShoesAdmin)
admin.site.register(Student, StudentAdmin)
