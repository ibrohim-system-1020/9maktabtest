from django.db import models
from apps.academics.models import Classroom, Subject, TeacherProfile, StudentProfile, Term

class Assessment(models.Model):
    TYPE_CHOICES = (
        ('daily', 'Kundalik baholash'),
        ('quiz', 'Nazorat ishi / Test'),
        ('practical', 'Amaliy ish / Laboratoriya'),
        ('midterm', 'Oraliq baholash (BSB)'),
        ('final_exam', 'Yakuniy baholash (CHSB)'),
    )

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assessments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assessments')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='assessments')
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=200, help_text="Masalan: 1-BSB yoki 2-Chorak test")
    assessment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='daily')
    date = models.DateField()
    max_score = models.DecimalField(max_digits=5, decimal_places=1, default=100.0)
    weight = models.DecimalField(max_digits=4, decimal_places=2, default=1.00, help_text="Bahoning salmog'i")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Baholash sinovi"
        verbose_name_plural = "Baholash sinovlari"
        ordering = ['-date']

    def __str__(self):
        return f"{self.classroom.name} | {self.subject.name} - {self.title} ({self.date})"

class AssessmentResult(models.Model):
    GRADE_CHOICES = (
        (5, "5 (A'lo)"),
        (4, "4 (Yaxshi)"),
        (3, "3 (Qoniqarli)"),
        (2, "2 (Qoniqarsiz)"),
    )

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='assessment_results')
    score = models.DecimalField(max_digits=5, decimal_places=1, help_text="To'plangan ball (0 dan max_score gacha)")
    grade_number = models.PositiveSmallIntegerField(choices=GRADE_CHOICES, help_text="Milliy baholash tizimi bo'yicha")
    remarks = models.CharField(max_length=255, blank=True, null=True, help_text="O'qituvchi izohi")
    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Baholash natijasi"
        verbose_name_plural = "Baholash natijalari"
        unique_together = ('assessment', 'student')
        ordering = ['student__user__last_name']

    def save(self, *args, **kwargs):
        # Auto-calculate standard Uzbekistan 5-point grade if not set
        if not self.grade_number and self.score is not None:
            max_s = float(self.assessment.max_score) if self.assessment else 100.0
            percent = (float(self.score) / max_s) * 100 if max_s > 0 else 0
            if percent >= 86:
                self.grade_number = 5
            elif percent >= 71:
                self.grade_number = 4
            elif percent >= 56:
                self.grade_number = 3
            else:
                self.grade_number = 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.user.get_full_name()}: {self.score} ball ({self.grade_number})"
