from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.assignments.serializers import AssignmentSerializer, AssignmentSubmissionSerializer
from apps.audit.models import AuditLog

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('classroom', 'subject', 'teacher__user').all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_school_admin:
            pass
        elif user.is_teacher_user:
            teacher = getattr(user, 'teacher_profile', None)
            if teacher:
                queryset = queryset.filter(teacher=teacher)
            else:
                queryset = queryset.none()
        elif user.is_student_user:
            student = getattr(user, 'student_profile', None)
            if student and student.classroom_id:
                queryset = queryset.filter(classroom_id=student.classroom_id, is_published=True)
            else:
                queryset = queryset.none()
        elif user.is_guardian_user:
            guardian = getattr(user, 'guardian_profile', None)
            if guardian:
                class_ids = guardian.student_relations.filter(is_verified=True).values_list('student__classroom_id', flat=True)
                queryset = queryset.filter(classroom_id__in=class_ids, is_published=True)
            else:
                queryset = queryset.none()

        classroom_id = self.request.query_params.get('classroom')
        subject_id = self.request.query_params.get('subject')
        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        teacher = getattr(user, 'teacher_profile', None)
        if teacher:
            instance = serializer.save(teacher=teacher)
        else:
            instance = serializer.save()
        AuditLog.objects.create(
            user=user,
            action='create',
            model_name='Assignment',
            object_id=str(instance.id),
            details=f"Yangi vazifa yaratildi: {instance.title} ({instance.classroom.name})"
        )

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.select_related('assignment', 'student__user').all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_school_admin:
            pass
        elif user.is_teacher_user:
            teacher = getattr(user, 'teacher_profile', None)
            if teacher:
                queryset = queryset.filter(assignment__teacher=teacher)
            else:
                queryset = queryset.none()
        elif user.is_student_user:
            student = getattr(user, 'student_profile', None)
            if student:
                queryset = queryset.filter(student=student)
            else:
                queryset = queryset.none()

        assignment_id = self.request.query_params.get('assignment')
        if assignment_id:
            queryset = queryset.filter(assignment_id=assignment_id)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        student = getattr(user, 'student_profile', None)
        if not student:
            raise permissions.exceptions.PermissionDenied("Faqat o'quvchilar vazifa topshira oladi.")
        
        # Check if submission is late
        assignment = serializer.validated_data['assignment']
        status_value = 'late' if timezone.now() > assignment.due_date else 'submitted'
        
        instance = serializer.save(student=student, status=status_value)
        AuditLog.objects.create(
            user=user,
            action='create',
            model_name='AssignmentSubmission',
            object_id=str(instance.id),
            details=f"O'quvchi {user.get_full_name()} vazifa topshirdi: {assignment.title}"
        )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def grade(self, request, pk=None):
        user = request.user
        if not (user.is_school_admin or user.is_teacher_user):
            return Response({'error': "Baholash huquqi mavjud emas."}, status=status.HTTP_403_FORBIDDEN)

        submission = self.get_object()
        score = request.data.get('score')
        feedback = request.data.get('feedback', '')

        if score is None:
            return Response({'error': "Ball ko‘rsatilishi shart."}, status=status.HTTP_400_BAD_REQUEST)

        submission.score = score
        submission.feedback = feedback
        submission.status = 'graded'
        submission.graded_by = user
        submission.graded_at = timezone.now()
        submission.save()

        AuditLog.objects.create(
            user=user,
            action='grade_entry',
            model_name='AssignmentSubmission',
            object_id=str(submission.id),
            details=f"Vazifa baholandi: {submission.student.user.get_full_name()} - {score} ball"
        )

        return Response({
            'message': "Vazifa muvaffaqiyatli baholandi.",
            'submission': AssignmentSubmissionSerializer(submission).data
        })
