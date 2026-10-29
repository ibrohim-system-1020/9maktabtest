from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    TYPE_CHOICES = (
        ('attendance', 'Davomat xabarnomasi'),
        ('grade', 'Baho qo‘yildi'),
        ('assignment', 'Yangi vazifa'),
        ('announcement', 'Umumiy e’lon'),
        ('system', 'Tizim xabari'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Xabarnoma"
        verbose_name_plural = "Xabarnomalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username} - {self.title} ({'O‘qilgan' if self.is_read else 'Yangi'})"
