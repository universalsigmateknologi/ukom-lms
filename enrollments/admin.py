from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Enrollment, LessonProgress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "course",
        "status",
        "enrolled_at",
        "completed_at",
        "progress_percentage",
        "view_progress",
    ]
    list_filter = ["status", "course"]
    search_fields = ["user__username", "user__email", "course__title"]
    list_editable = ["status"]
    list_per_page = 20

    @admin.display(description="Progres")
    def progress_percentage(self, obj):
        return f"{obj.progress_percentage}%"

    @admin.display(description="Detail Progres")
    def view_progress(self, obj):
        url = (
            reverse("admin:enrollments_lessonprogress_changelist")
            + f"?user__id__exact={obj.user.id}&lesson__module__course__id__exact={obj.course.id}"
        )
        return format_html(
            '<a href="{}" class="viewlink">Lihat</a>', url
        )


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