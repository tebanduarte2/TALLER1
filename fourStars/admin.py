from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['courses']
    ordering = ['first_name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    list_filter = ['professors']
    ordering = ['name']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student', 'professor', 'rating']
    search_fields = ['student', 'professor', 'rating']
    list_filter = ['rating']
    ordering = ['rating']


