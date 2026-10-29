from django.db import models
from django.conf import settings
from apps.academics.models import Subject

User = settings.AUTH_USER_MODEL

class LearningResource(models.Model):
    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF darslik / qo‘llanma'),
        ('doc', 'Hujjat (DOC/DOCX)'),
        ('presentation', 'Taqdimot (PPT/PPTX)'),
        ('video', 'Video dars'),
        ('link', 'Interaktiv havola / Simulyatsiya'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='resources')
    grade_level = models.PositiveSmallIntegerField(help_text="1 dan 11 gacha")
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='pdf')
    resource_url = models.CharField(max_length=500, help_text="Yuklab olish yoki ko'rish havolasi")
    file_size_mb = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_resources')
    downloads_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True, help_text="Ommaviy veb-saytda ko'rinadi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "O'quv resursi"
        verbose_name_plural = "O'quv resurslari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.subject.name}, {self.grade_level}-sinf)"
