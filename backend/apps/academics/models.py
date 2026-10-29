from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class AcademicYear(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Masalan: 2026-2027")
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=True)

    class Meta:
        verbose_name = "O'quv yili"
        verbose_name_plural = "O'quv yillari"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name}{' (Joriy)' if self.is_current else ''}"

class Term(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=50, help_text="Masalan: 1-Chorak")
    term_number = models.PositiveSmallIntegerField(choices=[
        (1, '1-Chorak'),
        (2, '2-Chorak'),
        (3, '3-Chorak'),
        (4, '4-Chorak'),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Chorak"
        verbose_name_plural = "Choraklar"
        unique_together = ('academic_year', 'term_number')
        ordering = ['academic_year', 'term_number']

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"

class Subject(models.Model):
    CATEGORY_CHOICES = (
        ('exact', 'Aniq fanlar'),
        ('natural', 'Tabiiy fanlar'),
        ('humanities', 'Ijtimoiy-gumanitar fanlar'),
        ('languages', 'Tillar va adabiyot'),
        ('arts_sports', 'Sanʼat, texnologiya va sport'),
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='exact')
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default='BookOpen')

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

class Classroom(models.Model):
    grade_level = models.PositiveSmallIntegerField(help_text="1 dan 11 gacha")
    section = models.CharField(max_length=5, help_text="A, B, V, G")
    name = models.CharField(max_length=20, help_text="Masalan: 9-A")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classrooms')
    class_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='directed_classes',
        help_text="Sinf rahbari"
    )
    room_number = models.CharField(max_length=20, blank=True, null=True, help_text="Dars xonasi raqami")
    max_capacity = models.PositiveSmallIntegerField(default=35)

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"
        unique_together = ('grade_level', 'section', 'academic_year')
        ordering = ['grade_level', 'section']

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=30, unique=True)
    qualification = models.CharField(max_length=100, default="Oliy toifali o'qituvchi")
    specialization = models.CharField(max_length=150, help_text="Masalan: Matematika va Informatika")
    hire_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    room_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "O'qituvchi profili"
        verbose_name_plural = "O'qituvchilar profillari"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.specialization}"

class StudentProfile(models.Model):
    GENDER_CHOICES = (
        ('male', "O'g'il bola"),
        ('female', "Qiz bola"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    student_id = models.CharField(max_length=30, unique=True, help_text="Masalan: 9M-2026-001")
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    enrollment_date = models.DateField(null=True, blank=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    medical_notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "O'quvchi profili"
        verbose_name_plural = "O'quvchilar profillari"

    def __str__(self):
        class_name = self.classroom.name if self.classroom else "Sinfi yo'q"
        return f"{self.user.get_full_name() or self.user.username} ({class_name})"

class GuardianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guardian_profile')
    occupation = models.CharField(max_length=150, blank=True, null=True)
    workplace = models.CharField(max_length=200, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Ota-ona profili"
        verbose_name_plural = "Ota-onalar profillari"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

class StudentGuardianRelation(models.Model):
    RELATION_CHOICES = (
        ('father', 'Otasi'),
        ('mother', 'Onasi'),
        ('guardian', 'Qonuniy vasiy'),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='guardian_relations')
    guardian = models.ForeignKey(GuardianProfile, on_delete=models.CASCADE, related_name='student_relations')
    relationship = models.CharField(max_length=20, choices=RELATION_CHOICES, default='father')
    is_primary = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)

    class Meta:
        verbose_name = "O'quvchi va ota-ona bog'liqligi"
        verbose_name_plural = "O'quvchi va ota-ona bog'liqliklari"
        unique_together = ('student', 'guardian')

    def __str__(self):
        return f"{self.guardian.user.get_full_name()} -> {self.student.user.get_full_name()} ({self.get_relationship_display()})"

class TeacherClassSubject(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='teaching_assignments')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_assignments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    weekly_hours = models.PositiveSmallIntegerField(default=2)

    class Meta:
        verbose_name = "O'qituvchi fan biriktiruvi"
        verbose_name_plural = "O'qituvchi fan biriktiruvlari"
        unique_together = ('teacher', 'classroom', 'subject', 'academic_year')

    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.classroom.name} ({self.subject.name})"
