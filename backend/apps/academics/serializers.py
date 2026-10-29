from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.academics.models import (
    AcademicYear, Term, Subject, Classroom,
    TeacherProfile, StudentProfile, GuardianProfile,
    StudentGuardianRelation, TeacherClassSubject
)
from apps.accounts.serializers import UserSerializer

User = get_user_model()

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)

    class Meta:
        model = Term
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    class_teacher_name = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = '__all__'

    def get_class_teacher_name(self, obj):
        if obj.class_teacher:
            return obj.class_teacher.get_full_name() or obj.class_teacher.username
        return "Biriktirilmagan"

    def get_students_count(self, obj):
        return obj.students.count()

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    assigned_classes = serializers.SerializerMethodField()
    total_weekly_hours = serializers.SerializerMethodField()
    total_students_count = serializers.SerializerMethodField()
    directed_class_name = serializers.SerializerMethodField()

    class Meta:
        model = TeacherProfile
        fields = '__all__'

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_assigned_classes(self, obj):
        assignments = obj.teaching_assignments.select_related('classroom', 'subject').all()
        return [
            {
                'assignment_id': a.id,
                'classroom_id': a.classroom.id,
                'classroom_name': a.classroom.name,
                'grade_level': a.classroom.grade_level,
                'subject_id': a.subject.id,
                'subject_name': a.subject.name,
                'weekly_hours': a.weekly_hours,
            }
            for a in assignments
        ]

    def get_total_weekly_hours(self, obj):
        return sum(obj.teaching_assignments.values_list('weekly_hours', flat=True))

    def get_total_students_count(self, obj):
        class_ids = obj.teaching_assignments.values_list('classroom_id', flat=True).distinct()
        return StudentProfile.objects.filter(classroom_id__in=class_ids).count()

    def get_directed_class_name(self, obj):
        d_class = obj.user.directed_classes.first()
        return d_class.name if d_class else None

class TeacherCreateUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True, default='')
    phone_number = serializers.CharField(required=False, allow_blank=True, default='')
    password = serializers.CharField(required=False, write_only=True, min_length=6, default='')
    employee_id = serializers.CharField(required=True, max_length=50)
    qualification = serializers.CharField(required=False, default="Oliy toifali o'qituvchi")
    specialization = serializers.CharField(required=True, max_length=150)
    room_number = serializers.CharField(required=False, allow_blank=True, default='')
    hire_date = serializers.DateField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True, default='')
    is_active = serializers.BooleanField(required=False, default=True)

    def validate_username(self, value):
        instance = getattr(self, 'instance', None)
        existing = User.objects.filter(username__iexact=value)
        if instance:
            existing = existing.exclude(id=instance.user.id)
        if existing.exists():
            raise serializers.ValidationError("Ushbu login band.")
        return value

    def validate_employee_id(self, value):
        instance = getattr(self, 'instance', None)
        existing = TeacherProfile.objects.filter(employee_id__iexact=value)
        if instance:
            existing = existing.exclude(id=instance.id)
        if existing.exists():
            raise serializers.ValidationError("Ushbu xodim ID raqami allaqachon mavjud.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            password = validated_data.pop('password', None) or "Teacher123!"
            user = User.objects.create_user(
                username=validated_data.pop('username'),
                first_name=validated_data.pop('first_name'),
                last_name=validated_data.pop('last_name'),
                email=validated_data.pop('email', ''),
                phone_number=validated_data.pop('phone_number', ''),
                is_active=validated_data.pop('is_active', True),
                role=User.ROLE_TEACHER,
                password=password,
                is_verified=True
            )
            profile = TeacherProfile.objects.create(
                user=user,
                **validated_data
            )
            return profile

    def update(self, instance, validated_data):
        with transaction.atomic():
            user = instance.user
            user.first_name = validated_data.get('first_name', user.first_name)
            user.last_name = validated_data.get('last_name', user.last_name)
            user.email = validated_data.get('email', user.email)
            user.phone_number = validated_data.get('phone_number', user.phone_number)
            if 'is_active' in validated_data:
                user.is_active = validated_data['is_active']
            new_password = validated_data.get('password')
            if new_password:
                user.set_password(new_password)
            user.save()

            instance.employee_id = validated_data.get('employee_id', instance.employee_id)
            instance.qualification = validated_data.get('qualification', instance.qualification)
            instance.specialization = validated_data.get('specialization', instance.specialization)
            instance.room_number = validated_data.get('room_number', instance.room_number)
            instance.hire_date = validated_data.get('hire_date', instance.hire_date)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.save()
            return instance

class GuardianProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    linked_children = serializers.SerializerMethodField()

    class Meta:
        model = GuardianProfile
        fields = '__all__'

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_linked_children(self, obj):
        relations = obj.student_relations.select_related('student__user', 'student__classroom').all()
        return [
            {
                'student_id': r.student.id,
                'student_code': r.student.student_id,
                'full_name': r.student.user.get_full_name() or r.student.user.username,
                'classroom': r.student.classroom.name if r.student.classroom else None,
                'relationship': r.get_relationship_display(),
                'is_verified': r.is_verified,
            }
            for r in relations
        ]

class TeacherClassSubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = TeacherClassSubject
        fields = '__all__'
