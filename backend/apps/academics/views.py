from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from apps.academics.models import (
    AcademicYear, Term, Subject, Classroom,
    TeacherProfile, StudentProfile, GuardianProfile,
    StudentGuardianRelation, TeacherClassSubject
)
from apps.academics.serializers import (
    AcademicYearSerializer, TermSerializer, SubjectSerializer,
    ClassroomSerializer, StudentProfileSerializer,
    TeacherProfileSerializer, TeacherCreateUpdateSerializer,
    GuardianProfileSerializer, TeacherClassSubjectSerializer
)
from apps.accounts.permissions import IsSchoolAdminUser, ReadOnlyOrAdmin
from apps.audit.models import AuditLog
from apps.assignments.models import Assignment, AssignmentSubmission

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [ReadOnlyOrAdmin]

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [ReadOnlyOrAdmin]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(code__icontains=search))
        return queryset

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.select_related('academic_year', 'class_teacher').prefetch_related('students').all()
    serializer_class = ClassroomSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        grade = self.request.query_params.get('grade')
        if grade:
            queryset = queryset.filter(grade_level=grade)
        return queryset

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user', 'classroom').all().order_by('student_id')
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Role-based scoping
        if user.is_school_admin:
            pass  # Admin sees all
        elif user.is_teacher_user:
            teacher_profile = getattr(user, 'teacher_profile', None)
            if teacher_profile:
                class_ids = teacher_profile.teaching_assignments.values_list('classroom_id', flat=True)
                directed_class_ids = user.directed_classes.values_list('id', flat=True)
                all_class_ids = set(list(class_ids) + list(directed_class_ids))
                queryset = queryset.filter(classroom_id__in=all_class_ids)
            else:
                queryset = queryset.none()
        elif user.is_guardian_user:
            guardian_profile = getattr(user, 'guardian_profile', None)
            if guardian_profile:
                student_ids = guardian_profile.student_relations.filter(is_verified=True).values_list('student_id', flat=True)
                queryset = queryset.filter(id__in=student_ids)
            else:
                queryset = queryset.none()
        elif user.is_student_user:
            queryset = queryset.filter(user=user)
        else:
            queryset = queryset.none()

        classroom_id = self.request.query_params.get('classroom')
        search = self.request.query_params.get('search')
        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(student_id__icontains=search)
            )
        return queryset

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.select_related('user').prefetch_related('teaching_assignments__classroom', 'teaching_assignments__subject').all().order_by('user__last_name')
    permission_classes = [ReadOnlyOrAdmin]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeacherCreateUpdateSerializer
        return TeacherProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        specialization = self.request.query_params.get('specialization')
        is_active = self.request.query_params.get('is_active')

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(specialization__icontains=search) |
                Q(employee_id__icontains=search)
            )
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        if is_active is not None and is_active != '':
            queryset = queryset.filter(user__is_active=is_active.lower() in ['true', '1'])

        return queryset

    def perform_create(self, serializer):
        profile = serializer.save()
        AuditLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action='create',
            model_name='TeacherProfile',
            object_id=str(profile.id),
            details=f"Yangi o'qituvchi qo'shildi: {profile.user.get_full_name()} ({profile.specialization})"
        )

    def perform_update(self, serializer):
        profile = serializer.save()
        AuditLog.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            action='update',
            model_name='TeacherProfile',
            object_id=str(profile.id),
            details=f"O'qituvchi ma'lumotlari yangilandi: {profile.user.get_full_name()}"
        )

    @action(detail=True, methods=['post'], permission_classes=[IsSchoolAdminUser])
    def toggle_active(self, request, pk=None):
        teacher = self.get_object()
        user = teacher.user
        user.is_active = not user.is_active
        user.save()
        status_text = "faollashtirildi" if user.is_active else "faolsizlantirildi"
        AuditLog.objects.create(
            user=request.user,
            action='update',
            model_name='TeacherProfile',
            object_id=str(teacher.id),
            details=f"O'qituvchi {user.get_full_name()} {status_text}."
        )
        return Response({
            'message': f"O'qituvchi muvaffaqiyatli {status_text}.",
            'is_active': user.is_active
        })

    @action(detail=True, methods=['post'], permission_classes=[IsSchoolAdminUser])
    def assign_class(self, request, pk=None):
        teacher = self.get_object()
        classroom_id = request.data.get('classroom_id')
        subject_id = request.data.get('subject_id')
        weekly_hours = request.data.get('weekly_hours', 2)

        try:
            classroom = Classroom.objects.get(id=classroom_id)
            subject = Subject.objects.get(id=subject_id)
            current_year = AcademicYear.objects.filter(is_current=True).first() or AcademicYear.objects.first()
        except (Classroom.DoesNotExist, Subject.DoesNotExist):
            return Response({'error': "Sinf yoki fan topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        assignment, created = TeacherClassSubject.objects.update_or_create(
            teacher=teacher,
            classroom=classroom,
            subject=subject,
            academic_year=current_year,
            defaults={'weekly_hours': weekly_hours}
        )
        AuditLog.objects.create(
            user=request.user,
            action='create',
            model_name='TeacherClassSubject',
            object_id=str(assignment.id),
            details=f"O'qituvchi {teacher.user.get_full_name()} ga {classroom.name} sinfi {subject.name} fani biriktirildi."
        )
        return Response({
            'message': f"{classroom.name} sinfida {subject.name} fani muvaffaqiyatli biriktirildi.",
            'assignment_id': assignment.id
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_classes(self, request):
        user = request.user
        teacher = getattr(user, 'teacher_profile', None)
        if not teacher:
            return Response({'error': "Foydalanuvchi o'qituvchi emas"}, status=status.HTTP_400_BAD_REQUEST)
        
        assignments = teacher.teaching_assignments.select_related('classroom', 'subject').all()
        directed_classes = user.directed_classes.all()
        
        assigned_data = [
            {
                'classroom_id': a.classroom.id,
                'classroom_name': a.classroom.name,
                'grade_level': a.classroom.grade_level,
                'subject_id': a.subject.id,
                'subject_name': a.subject.name,
                'weekly_hours': a.weekly_hours,
                'is_class_teacher': (a.classroom.class_teacher_id == user.id)
            }
            for a in assignments
        ]
        directed_data = [
            {
                'classroom_id': c.id,
                'classroom_name': c.name,
                'grade_level': c.grade_level,
                'room_number': c.room_number,
                'students_count': c.students.count()
            }
            for c in directed_classes
        ]
        return Response({
            'subject_assignments': assigned_data,
            'directed_classes': directed_data
        })

class GuardianProfileViewSet(viewsets.ModelViewSet):
    queryset = GuardianProfile.objects.select_related('user').all()
    serializer_class = GuardianProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_children(self, request):
        user = request.user
        guardian = getattr(user, 'guardian_profile', None)
        if not guardian:
            return Response({'error': "Foydalanuvchi ota-ona emas"}, status=status.HTTP_400_BAD_REQUEST)
        
        relations = guardian.student_relations.filter(is_verified=True).select_related('student__user', 'student__classroom')
        children_data = [
            {
                'relation_id': r.id,
                'student_id': r.student.id,
                'student_code': r.student.student_id,
                'full_name': r.student.user.get_full_name() or r.student.user.username,
                'classroom_id': r.student.classroom.id if r.student.classroom else None,
                'classroom_name': r.student.classroom.name if r.student.classroom else "Biriktirilmagan",
                'relationship': r.get_relationship_display(),
                'birth_date': r.student.birth_date,
            }
            for r in relations
        ]
        return Response(children_data)

class TeacherClassSubjectViewSet(viewsets.ModelViewSet):
    queryset = TeacherClassSubject.objects.select_related('teacher__user', 'classroom', 'subject').all()
    serializer_class = TeacherClassSubjectSerializer
    permission_classes = [ReadOnlyOrAdmin]
