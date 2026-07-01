from django.contrib import admin
from .models import Category, Course, Module, Lesson


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 20


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ["title", "description", "order"]
    ordering = ["order"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "title", 
        "category", 
        "instructor", 
        "level", 
        "status", 
        "total_duration",
        "created_at",
    ]
    list_filter = ["status", "level", "category"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["status"]
    inlines = [ModuleInline]
    list_per_page = 20


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ["title", "content_type", "duration", "order", "is_preview"]
    ordering = ["order"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "order", "total_lessons", "total_duration"]
    list_filter = ["course"]
    search_fields = ["title", "course__title"]
    inlines = [LessonInline]
    list_per_page = 20


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "module",
        "content_type",
        "duration",
        "order",
        "is_preview",
        "created_at",
    ]
    list_filter = ["content_type", "module__course"]
    search_fields = ["title", "module__title"]
    list_editable = ["is_preview", "order"]
    list_per_page = 20