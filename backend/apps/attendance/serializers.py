from rest_framework import serializers
from apps.attendance.models import AttendanceSession, AttendanceRecord

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_code = serializers.CharField(source='student.student_id', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = '__all__'

class AttendanceSessionSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    term_name = serializers.CharField(source='term.name', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)
    records = AttendanceRecordSerializer(many=True, read_only=True)
    total_present = serializers.SerializerMethodField()
    total_absent = serializers.SerializerMethodField()
    total_late = serializers.SerializerMethodField()
    total_excused = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSession
        fields = '__all__'

    def get_total_present(self, obj):
        return obj.records.filter(status='present').count()

    def get_total_absent(self, obj):
        return obj.records.filter(status='absent').count()

    def get_total_late(self, obj):
        return obj.records.filter(status='late').count()

    def get_total_excused(self, obj):
        return obj.records.filter(status='excused').count()

class BulkAttendanceItemSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=AttendanceRecord.STATUS_CHOICES)
    reason = serializers.CharField(required=False, allow_blank=True, default="")

class BulkAttendanceSubmissionSerializer(serializers.Serializer):
    classroom_id = serializers.IntegerField()
    date = serializers.DateField()
    term_id = serializers.IntegerField(required=False)
    records = BulkAttendanceItemSerializer(many=True)
