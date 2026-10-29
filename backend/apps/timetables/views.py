from rest_framework import viewsets, permissions
from apps.timetables.models import TimetableEntry
from apps.timetables.serializers import TimetableEntrySerializer
from apps.accounts.permissions import ReadOnlyOrAdmin

class TimetableEntryViewSet(viewsets.ModelViewSet):
    queryset = TimetableEntry.objects.select_related(
        'classroom', 'subject', 'teacher__user', 'academic_year'
    ).all()
    serializer_class = TimetableEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        classroom_id = self.request.query_params.get('classroom')
        teacher_id = self.request.query_params.get('teacher')
        day_of_week = self.request.query_params.get('day')
        
        # Automatic scoping for student if no class specified
        if user.is_student_user and not classroom_id:
            student_profile = getattr(user, 'student_profile', None)
            if student_profile and student_profile.classroom_id:
                queryset = queryset.filter(classroom_id=student_profile.classroom_id)
            else:
                queryset = queryset.none()
        elif user.is_teacher_user and not classroom_id and not teacher_id:
            teacher_profile = getattr(user, 'teacher_profile', None)
            if teacher_profile:
                queryset = queryset.filter(teacher=teacher_profile)

        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)

        return queryset.order_by('day_of_week', 'period_number')
