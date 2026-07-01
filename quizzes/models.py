from django.db import models


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ("multiple_choice", "Pilihan Ganda"),
        ("true_false", "Benar/Salah"),
    ]

    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Materi Kuis",
        limit_choices_to={"content_type": "quiz"},
    )
    question_text = models.TextField(verbose_name="Teks Soal")
    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPE_CHOICES,
        default="multiple_choice", verbose_name="Tipe Soal"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Urutan")
    explanation = models.TextField(
        blank=True, verbose_name="Penjelasan",
        help_text="Akan ditampilkan setelah user menjawab"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Soal"
        verbose_name_plural = "Soal"
        ordering = ["lesson", "order"]
        unique_together = ["lesson", "order"]

    def __str__(self):
        return f"{self.lesson.title} - Soal #{self.order}"


class Choice(models.Model):  # ✅ PERBAIKAN DI SINI
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name="Soal",
    )
    choice_text = models.CharField(max_length=500, verbose_name="Teks Pilihan")
    is_correct = models.BooleanField(default=False, verbose_name="Jawaban Benar")
    order = models.PositiveIntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pilihan Jawaban"
        verbose_name_plural = "Pilihan Jawaban"
        ordering = ["question", "order"]
        unique_together = ["question", "order"]

    def __str__(self):
        return f"{self.question} - {self.choice_text}"


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        verbose_name="User",
    )
    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        verbose_name="Materi Kuis",
    )
    score = models.PositiveIntegerField(default=0, verbose_name="Skor (%)")
    total_questions = models.PositiveIntegerField(default=0, verbose_name="Total Soal")
    correct_answers = models.PositiveIntegerField(default=0, verbose_name="Jawaban Benar")
    time_spent = models.PositiveIntegerField(
        default=0, verbose_name="Waktu Dihabiskan (detik)"
    )
    is_passed = models.BooleanField(default=False, verbose_name="Lulus")
    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Mulai")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Waktu Selesai")

    class Meta:
        verbose_name = "Percobaan Kuis"
        verbose_name_plural = "Percobaan Kuis"
        ordering = ["-attempted_at"]

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} ({self.score}%)"

    @property
    def attempt_number(self):
        return (
            QuizAttempt.objects.filter(
                user=self.user, lesson=self.lesson,
                attempted_at__lte=self.attempted_at
            ).count()
        )


class UserAnswer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Percobaan",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="user_answers",
        verbose_name="Soal",
    )
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Jawaban Dipilih",
        help_text="Kosongkan jika tidak dijawab",
    )
    is_correct = models.BooleanField(default=False, verbose_name="Jawaban Benar")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Jawaban User"
        verbose_name_plural = "Jawaban User"
        unique_together = ["attempt", "question"]

    def __str__(self):
        choice_text = self.selected_choice.choice_text if self.selected_choice else "Tidak dijawab"
        return f"{self.attempt} - {self.question} → {choice_text}"