from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from apps.attendance.models import AttendanceSession, AttendanceRecord
from apps.attendance.serializers import (
    AttendanceSessionSerializer,
    AttendanceRecordSerializer,
    BulkAttendanceSubmissionSerializer
)
from apps.academics.models import Classroom, StudentProfile, Term
from apps.audit.models import AuditLog

class AttendanceSessionViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSession.objects.select_related('classroom', 'term', 'recorded_by').prefetch_related('records__student__user').all()
    serializer_class = AttendanceSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        classroom_id = self.request.query_params.get('classroom')
        date = self.request.query_params.get('date')

        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if date:
            queryset = queryset.filter(date=date)

        return queryset

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def save_bulk(self, request):
        user = request.user
        # Allow teachers and admins
        if not (user.is_school_admin or user.is_teacher_user):
            return Response({'error': "Davomat kiritish uchun ruxsat yo‘q."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BulkAttendanceSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        classroom_id = serializer.validated_data['classroom_id']
        date = serializer.validated_data['date']
        term_id = serializer.validated_data.get('term_id')
        records_data = serializer.validated_data['records']

        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            return Response({'error': "Sinf topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        if not term_id:
            current_term = Term.objects.filter(is_current=True).first() or Term.objects.first()
            term_id = current_term.id if current_term else None

        with transaction.atomic():
            session, created = AttendanceSession.objects.update_or_create(
                classroom=classroom,
                date=date,
                defaults={
                    'term_id': term_id,
                    'recorded_by': user,
                }
            )

            for item in records_data:
                AttendanceRecord.objects.update_or_create(
                    session=session,
                    student_id=item['student_id'],
                    defaults={
                        'status': item['status'],
                        'reason': item.get('reason', ''),
                    }
                )

            # Audit log
            AuditLog.objects.create(
                user=user,
                action='attendance_entry',
                model_name='AttendanceSession',
                object_id=str(session.id),
                details=f"{classroom.name} sinfi uchun {date} sanasida {len(records_data)} ta o‘quvchiga davomat saqlandi."
            )

        return Response({
            'message': "Davomat muvaffaqiyatli saqlandi.",
            'session_id': session.id,
            'records_count': len(records_data)
        }, status=status.HTTP_200_OK)

class AttendanceRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AttendanceRecord.objects.select_related('session__classroom', 'student__user').all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_school_admin:
            pass
        elif user.is_teacher_user:
            teacher_profile = getattr(user, 'teacher_profile', None)
            if teacher_profile:
                class_ids = teacher_profile.teaching_assignments.values_list('classroom_id', flat=True)
                queryset = queryset.filter(session__classroom_id__in=class_ids)
            else:
                queryset = queryset.none()
        elif user.is_guardian_user:
            guardian = getattr(user, 'guardian_profile', None)
            if guardian:
                student_ids = guardian.student_relations.filter(is_verified=True).values_list('student_id', flat=True)
                queryset = queryset.filter(student_id__in=student_ids)
            else:
                queryset = queryset.none()
        elif user.is_student_user:
            student = getattr(user, 'student_profile', None)
            if student:
                queryset = queryset.filter(student=student)
            else:
                queryset = queryset.none()

        student_id = self.request.query_params.get('student')
        classroom_id = self.request.query_params.get('classroom')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if classroom_id:
            queryset = queryset.filter(session__classroom_id=classroom_id)
        if start_date:
            queryset = queryset.filter(session__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(session__date__lte=end_date)

        return queryset.order_by('-session__date')
