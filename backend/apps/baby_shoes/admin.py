from django.contrib import admin
from .models import BabyShoes, Context, Question, Student, StudentResponse

# Register your models here.
# admin.site.register(BabyShoes)
# admin.site.register(Context)


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


class BabyShoesAdmin(admin.ModelAdmin):
    model = BabyShoes
    inlines = [ContextInline, QuestionInline]


admin.site.register(BabyShoes, BabyShoesAdmin)
admin.site.register(Student, StudentAdmin)
