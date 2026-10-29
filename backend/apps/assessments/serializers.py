from rest_framework import serializers
from apps.assessments.models import Assessment, AssessmentResult

class AssessmentResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_code = serializers.CharField(source='student.student_id', read_only=True)
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    subject_name = serializers.CharField(source='assessment.subject.name', read_only=True)
    grade_display = serializers.CharField(source='get_grade_number_display', read_only=True)

    class Meta:
        model = AssessmentResult
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    term_name = serializers.CharField(source='term.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    results_count = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = '__all__'

    def get_results_count(self, obj):
        return obj.results.count()

class BulkAssessmentItemSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    score = serializers.DecimalField(max_digits=5, decimal_places=1)
    grade_number = serializers.IntegerField(required=False, min_value=2, max_value=5)
    remarks = serializers.CharField(required=False, allow_blank=True, default="")

class BulkAssessmentSaveSerializer(serializers.Serializer):
    assessment_id = serializers.IntegerField()
    results = BulkAssessmentItemSerializer(many=True)
