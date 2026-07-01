from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    icon = models.CharField(
        max_length=50, blank=True, verbose_name="Icon",
        help_text="Contoh: fas fa-code, fas fa-paint-brush"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Pemula"),
        ("intermediate", "Menengah"),
        ("advanced", "Lanjutan"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Dipublikasi"),
        ("archived", "Diarsipkan"),
    ]

    title = models.CharField(max_length=200, verbose_name="Judul")
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    description = models.TextField(verbose_name="Deskripsi")
    thumbnail = models.ImageField(
        upload_to="courses/thumbnails/", blank=True, null=True, verbose_name="Thumbnail"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="courses", verbose_name="Kategori"
    )
    instructor = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="courses_taught",
        verbose_name="Instruktur", limit_choices_to={"is_staff": True}
    )
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default="beginner", verbose_name="Level"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft", verbose_name="Status"
    )
    total_duration = models.IntegerField(default=0, verbose_name="Total Durasi (menit)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui")

    class Meta:
        verbose_name = "Kursus"
        verbose_name_plural = "Kursus"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def total_modules(self):
        return self.modules.count()

    @property
    def total_lessons(self):
        return Lesson.objects.filter(module__course=self).count()

    @property
    def total_students(self):
        return self.enrollments.filter(status="active").count()


class Module(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="modules", verbose_name="Kursus"
    )
    title = models.CharField(max_length=200, verbose_name="Judul Module")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    order = models.PositiveIntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Module"
        ordering = ["course", "order"]
        unique_together = ["course", "order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    @property
    def total_lessons(self):
        return self.lessons.count()

    @property
    def total_duration(self):
        return self.lessons.aggregate(total=models.Sum("duration"))["total"] or 0


class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = [
        ("video", "Video"),
        ("text", "Teks"),
        ("article", "Artikel"),
        ("quiz", "Kuis"),
    ]

    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons", verbose_name="Module"
    )
    title = models.CharField(max_length=200, verbose_name="Judul Materi")
    content_type = models.CharField(
        max_length=20, choices=CONTENT_TYPE_CHOICES, default="text", verbose_name="Tipe Konten"
    )
    content = models.TextField(blank=True, verbose_name="Konten")
    video_url = models.URLField(blank=True, verbose_name="URL Video")
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name="Durasi (menit)")
    order = models.PositiveIntegerField(default=0, verbose_name="Urutan")
    is_preview = models.BooleanField(default=False, verbose_name="Bisa Di-preview")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ========== FIELD KUIS ==========
    time_limit = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Batas Waktu (menit)",
        help_text="Kosongkan jika tidak ada batas waktu"
    )
    passing_grade = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Nilai Minimum (%)",
        help_text="Kosongkan jika tidak ada syarat kelulusan"
    )
    max_attempts = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Maks Percobaan",
        help_text="Kosongkan jika tidak terbatas"
    )
    shuffle_questions = models.BooleanField(
        default=False, verbose_name="Acak Urutan Soal"
    )
    shuffle_choices = models.BooleanField(
        default=False, verbose_name="Acak Urutan Pilihan Jawaban"
    )

    class Meta:
        verbose_name = "Materi"
        verbose_name_plural = "Materi"
        ordering = ["module", "order"]
        unique_together = ["module", "order"]

    def __str__(self):
        return f"{self.module.title} - {self.title}"

    @property
    def is_quiz(self):
        return self.content_type == "quiz"

    @property
    def total_questions(self):
        if self.is_quiz:
            from quizzes.models import Question
            return Question.objects.filter(lesson=self).count()
        return 0