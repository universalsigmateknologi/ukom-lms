from django.db import models


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("active", "Aktif"),
        ("completed", "Selesai"),
        ("dropped", "Keluar"),
    ]

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="User",
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Kursus",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Daftar")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tanggal Selesai")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active", verbose_name="Status"
    )

    class Meta:
        verbose_name = "Pendaftaran"
        verbose_name_plural = "Pendaftaran"
        unique_together = ["user", "course"]
        ordering = ["-enrolled_at"]

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    @property
    def progress_percentage(self):
        """Hitung persentase progres berdasarkan lesson yang sudah selesai."""
        from courses.models import Lesson

        total_lessons = Lesson.objects.filter(module__course=self.course).count()
        if total_lessons == 0:
            return 0

        completed = self.lesson_progresses.filter(is_completed=True).count()
        return int((completed / total_lessons) * 100)


class LessonProgress(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="lesson_progresses",
        verbose_name="User",
    )
    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE,
        related_name="progresses",
        verbose_name="Materi",
    )
    is_completed = models.BooleanField(default=False, verbose_name="Selesai")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tanggal Selesai")
    last_accessed = models.DateTimeField(null=True, blank=True, verbose_name="Terakhir Diakses")

    class Meta:
        verbose_name = "Progres Materi"
        verbose_name_plural = "Progres Materi"
        unique_together = ["user", "lesson"]
        ordering = ["-last_accessed"]

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"