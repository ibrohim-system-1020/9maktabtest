from rest_framework import serializers
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.academics.models import StudentProfile

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_code = serializers.CharField(source='student.student_id', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = '__all__'
        read_only_fields = ['id', 'student', 'submitted_at', 'graded_at', 'graded_by']

class AssignmentSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    submissions_count = serializers.SerializerMethodField()
    my_submission = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ['id', 'teacher', 'created_at', 'updated_at']

    def get_submissions_count(self, obj):
        return obj.submissions.count()

    def get_my_submission(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.is_student_user:
            student = getattr(request.user, 'student_profile', None)
            if student:
                sub = obj.submissions.filter(student=student).first()
                if sub:
                    return AssignmentSubmissionSerializer(sub).data
        return None
