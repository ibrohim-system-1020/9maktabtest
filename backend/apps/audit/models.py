from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class AuditLog(models.Model):
    ACTION_CHOICES = (
        ('login', 'Tizimga kirish'),
        ('logout', 'Tizimdan chiqish'),
        ('create', 'Yangi yaratildi'),
        ('update', 'Tahrirlandi'),
        ('delete', 'O‘chirildi'),
        ('grade_entry', 'Baho qo‘yildi'),
        ('attendance_entry', 'Davomat belgilandi'),
        ('export_csv', 'Ma’lumot eksport qilindi'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Audit yozuvi"
        verbose_name_plural = "Audit yozuvlari"
        ordering = ['-timestamp']

    def __str__(self):
        user_name = self.user.username if self.user else "Anonim"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {user_name} - {self.get_action_display()} ({self.model_name})"
