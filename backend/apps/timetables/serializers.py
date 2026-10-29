from rest_framework import serializers
from apps.timetables.models import TimetableEntry

class TimetableEntrySerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    subject_icon = serializers.CharField(source='subject.icon', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = TimetableEntry
        fields = '__all__'
