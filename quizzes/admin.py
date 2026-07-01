from django.contrib import admin
from .models import Question, Choice, QuizAttempt, UserAnswer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    fields = ["choice_text", "is_correct", "order"]
    ordering = ["order"]
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "question_text_short", "lesson", "question_type", "order", "total_choices", "created_at"
    ]
    list_filter = ["question_type", "lesson__module__course"]
    search_fields = ["question_text", "lesson__title"]
    inlines = [ChoiceInline]
    list_per_page = 20

    fieldsets = (
        ("Soal", {
            "fields": ("lesson", "question_text", "question_type", "order")
        }),
        ("Penjelasan", {
            "fields": ("explanation",),
            "classes": ("wide",),
        }),
    )

    @admin.display(description="Teks Soal")
    def question_text_short(self, obj):
        return obj.question_text[:80] + "..." if len(obj.question_text) > 80 else obj.question_text

    @admin.display(description="Jumlah Pilihan")
    def total_choices(self, obj):
        return obj.choices.count()


class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ["question", "selected_choice", "is_correct"]
    can_delete = False
    max_num = 0


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = [
        "user", "lesson", "attempt_number", "score", "total_questions",
        "correct_answers", "time_spent_formatted", "is_passed", "attempted_at",
    ]
    list_filter = ["is_passed", "lesson__module__course"]
    search_fields = ["user__username", "user__email", "lesson__title"]
    inlines = [UserAnswerInline]
    list_per_page = 20

    @admin.display(description="Percobaan Ke")
    def attempt_number(self, obj):
        return obj.attempt_number

    @admin.display(description="Waktu")
    def time_spent_formatted(self, obj):
        minutes, seconds = divmod(obj.time_spent, 60)
        return f"{minutes:02d}:{seconds:02d}"


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = [
        "attempt", "question", "selected_choice", "is_correct", "created_at"
    ]
    list_filter = ["is_correct", "attempt__lesson"]
    search_fields = ["question__question_text", "attempt__user__username"]
    list_per_page = 20