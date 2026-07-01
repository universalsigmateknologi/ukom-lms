from django.contrib import admin
from .models import Enrollment, LessonProgress


class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0
    readonly_fields = ["lesson", "is_completed", "completed_at", "last_accessed"]
    can_delete = False
    max_num = 0


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "course",
        "status",
        "enrolled_at",
        "completed_at",
        "progress_percentage",
    ]
    list_filter = ["status", "course"]
    search_fields = ["user__username", "user__email", "course__title"]
    list_editable = ["status"]
    inlines = [LessonProgressInline]
    list_per_page = 20


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "lesson",
        "is_completed",
        "completed_at",
        "last_accessed",
    ]
    list_filter = ["is_completed", "lesson__module__course"]
    search_fields = ["user__username", "lesson__title"]
    list_editable = ["is_completed"]
    list_per_page = 20