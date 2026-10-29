from django.db import models
from django.conf import settings
from apps.academics.models import Classroom, Subject, TeacherProfile, StudentProfile, Term

User = settings.AUTH_USER_MODEL

class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='assignments')
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Topshiriq matni va ko'rsatmalar")
    attachment_url = models.CharField(max_length=500, blank=True, null=True, help_text="Qo'shimcha fayl havolasi")
    max_score = models.PositiveIntegerField(default=100)
    due_date = models.DateTimeField(help_text="Topshirishning oxirgi muddati")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.classroom.name} | {self.subject.name}: {self.title}"

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Topshirildi'),
        ('graded', 'Baholandi'),
        ('late', 'Kech topshirildi'),
        ('returned', 'Qaytarildi'),
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='submissions')
    submission_text = models.TextField(blank=True, null=True, help_text="O'quvchi javobi")
    file_url = models.CharField(max_length=500, blank=True, null=True, help_text="Yuborilgan fayl havolasi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    score = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True, help_text="O'qituvchi izohi")
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Topshirilgan vazifa"
        verbose_name_plural = "Topshirilgan vazifalar"
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.user.get_full_name()} -> {self.assignment.title} ({self.get_status_display()})"
