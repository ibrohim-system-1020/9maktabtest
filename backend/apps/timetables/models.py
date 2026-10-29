from django.db import models
from apps.academics.models import Classroom, Subject, TeacherProfile, AcademicYear, Term

class TimetableEntry(models.Model):
    DAY_CHOICES = (
        (1, 'Dushanba'),
        (2, 'Seshanba'),
        (3, 'Chorshanba'),
        (4, 'Payshanba'),
        (5, 'Juma'),
        (6, 'Shanba'),
    )

    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetable_entries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='timetable_entries')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.SET_NULL, null=True, blank=True)
    day_of_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    period_number = models.PositiveSmallIntegerField(help_text="Dars soati: 1 dan 7 gacha")
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Dars jadvali yozuvi"
        verbose_name_plural = "Dars jadvali yozuvlari"
        unique_together = ('classroom', 'academic_year', 'day_of_week', 'period_number')
        ordering = ['day_of_week', 'period_number']

    def __str__(self):
        return f"{self.classroom.name} | {self.get_day_of_week_display()} {self.period_number}-para: {self.subject.name}"
