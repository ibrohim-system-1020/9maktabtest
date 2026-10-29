from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from apps.assessments.models import Assessment, AssessmentResult
from apps.assessments.serializers import (
    AssessmentSerializer,
    AssessmentResultSerializer,
    BulkAssessmentSaveSerializer
)
from apps.audit.models import AuditLog

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.select_related('classroom', 'subject', 'teacher__user', 'term').all()
    serializer_class = AssessmentSerializer
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
                queryset = queryset.filter(classroom_id=student.classroom_id)
            else:
                queryset = queryset.none()
        elif user.is_guardian_user:
            guardian = getattr(user, 'guardian_profile', None)
            if guardian:
                class_ids = guardian.student_relations.filter(is_verified=True).values_list('student__classroom_id', flat=True)
                queryset = queryset.filter(classroom_id__in=class_ids)
            else:
                queryset = queryset.none()

        classroom_id = self.request.query_params.get('classroom')
        subject_id = self.request.query_params.get('subject')
        term_id = self.request.query_params.get('term')

        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if term_id:
            queryset = queryset.filter(term_id=term_id)

        return queryset

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def save_bulk_results(self, request):
        user = request.user
        if not (user.is_school_admin or user.is_teacher_user):
            return Response({'error': "Baholarni kiritish huquqi yo‘q."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BulkAssessmentSaveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        assessment_id = serializer.validated_data['assessment_id']
        results_data = serializer.validated_data['results']

        try:
            assessment = Assessment.objects.get(id=assessment_id)
        except Assessment.DoesNotExist:
            return Response({'error': "Baholash sinovi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            for item in results_data:
                res, _ = AssessmentResult.objects.update_or_create(
                    assessment=assessment,
                    student_id=item['student_id'],
                    defaults={
                        'score': item['score'],
                        'grade_number': item.get('grade_number'),
                        'remarks': item.get('remarks', ''),
                    }
                )

            AuditLog.objects.create(
                user=user,
                action='grade_entry',
                model_name='Assessment',
                object_id=str(assessment.id),
                details=f"{assessment.classroom.name} sinfi {assessment.subject.name} fanidan {len(results_data)} ta o‘quvchiga baholar kiritildi."
            )

        return Response({
            'message': "Baholar muvaffaqiyatli saqlandi.",
            'assessment_id': assessment.id,
            'count': len(results_data)
        }, status=status.HTTP_200_OK)

class AssessmentResultViewSet(viewsets.ModelViewSet):
    queryset = AssessmentResult.objects.select_related('assessment__subject', 'assessment__classroom', 'student__user').all()
    serializer_class = AssessmentResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if user.is_school_admin:
            pass
        elif user.is_teacher_user:
            teacher = getattr(user, 'teacher_profile', None)
            if teacher:
                queryset = queryset.filter(assessment__teacher=teacher)
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
        assessment_id = self.request.query_params.get('assessment')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if assessment_id:
            queryset = queryset.filter(assessment_id=assessment_id)

        return queryset
