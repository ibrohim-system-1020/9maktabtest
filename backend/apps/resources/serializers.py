from rest_framework import serializers
from apps.resources.models import LearningResource

class LearningResourceSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)

    class Meta:
        model = LearningResource
        fields = '__all__'
        read_only_fields = ['id', 'downloads_count', 'created_at', 'updated_at']
