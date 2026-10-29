from rest_framework import serializers
from apps.portal.models import (
    SchoolInfo, Announcement, SchoolEvent,
    Achievement, GalleryItem, FAQ, PublicInquiry
)

class SchoolInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolInfo
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['id', 'views_count', 'published_at', 'updated_at']

class SchoolEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolEvent
        fields = '__all__'

class AchievementSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Achievement
        fields = '__all__'

class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class PublicInquirySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PublicInquiry
        fields = '__all__'
        read_only_fields = ['id', 'status', 'admin_response', 'created_at', 'resolved_at']

class PublicInquiryAdminSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = PublicInquiry
        fields = '__all__'
