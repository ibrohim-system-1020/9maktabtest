from django.db import models
from django.conf import settings
from apps.academics.models import Classroom, StudentProfile, Term

User = settings.AUTH_USER_MODEL

class AttendanceSession(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='attendance_sessions')
    date = models.DateField(help_text="Davomat olingan sana")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='attendance_sessions')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Davomat sessiyasi"
        verbose_name_plural = "Davomat sessiyalari"
        unique_together = ('classroom', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.classroom.name} davomati ({self.date})"

class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('present', 'Bor / Darsda'),
        ('absent', 'Sababsiz yo‘q'),
        ('late', 'Kechikkan'),
        ('excused', 'Sababli yo‘q'),
    )

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    reason = models.CharField(max_length=255, blank=True, null=True, help_text="Sabab yoki izoh")
    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Davomat qaydi"
        verbose_name_plural = "Davomat qaydlari"
        unique_together = ('session', 'student')
        ordering = ['student__user__last_name']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.get_status_display()}"
