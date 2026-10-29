from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_SUPER_ADMIN = 'super_admin'
    ROLE_SCHOOL_ADMIN = 'school_admin'
    ROLE_PRINCIPAL = 'principal'
    ROLE_TEACHER = 'teacher'
    ROLE_STUDENT = 'student'
    ROLE_GUARDIAN = 'guardian'

    ROLE_CHOICES = (
        (ROLE_SUPER_ADMIN, "Super Administrator"),
        (ROLE_SCHOOL_ADMIN, "Maktab Administratori"),
        (ROLE_PRINCIPAL, "Direktor / Rahbariyat"),
        (ROLE_TEACHER, "O'qituvchi"),
        (ROLE_STUDENT, "O'quvchi"),
        (ROLE_GUARDIAN, "Ota-ona / Vasiy"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        help_text="Foydalanuvchining tizimdagi roli"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="+998901234567 formatida")
    avatar = models.CharField(max_length=500, blank=True, null=True, help_text="Profil rasmi URL manzili")
    address = models.TextField(blank=True, null=True, help_text="Yashash manzili")
    is_verified = models.BooleanField(default=True, help_text="Hisob tasdiqlanganmi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-date_joined']

    def __str__(self):
        full_name = self.get_full_name()
        return f"{full_name} ({self.username}) - {self.get_role_display()}" if full_name else f"{self.username} - {self.get_role_display()}"

    @property
    def is_super_admin(self):
        return self.role == self.ROLE_SUPER_ADMIN or self.is_superuser

    @property
    def is_school_admin(self):
        return self.role in (self.ROLE_SUPER_ADMIN, self.ROLE_SCHOOL_ADMIN) or self.is_superuser

    @property
    def is_management(self):
        return self.role in (self.ROLE_SUPER_ADMIN, self.ROLE_SCHOOL_ADMIN, self.ROLE_PRINCIPAL) or self.is_superuser

    @property
    def is_teacher_user(self):
        return self.role == self.ROLE_TEACHER

    @property
    def is_student_user(self):
        return self.role == self.ROLE_STUDENT

    @property
    def is_guardian_user(self):
        return self.role == self.ROLE_GUARDIAN
