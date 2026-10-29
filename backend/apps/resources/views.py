from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from apps.resources.models import LearningResource
from apps.resources.serializers import LearningResourceSerializer
from apps.accounts.permissions import ReadOnlyOrAdmin

class LearningResourceViewSet(viewsets.ModelViewSet):
    queryset = LearningResource.objects.select_related('subject', 'uploaded_by').all()
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not (user and user.is_authenticated):
            queryset = queryset.filter(is_public=True)

        subject_id = self.request.query_params.get('subject')
        grade = self.request.query_params.get('grade')
        file_type = self.request.query_params.get('file_type')
        search = self.request.query_params.get('search')

        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        if grade:
            queryset = queryset.filter(grade_level=grade)
        if file_type:
            queryset = queryset.filter(file_type=file_type)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(subject__name__icontains=search)
            )

        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(uploaded_by=user if user.is_authenticated else None)

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def track_download(self, request, pk=None):
        resource = self.get_object()
        LearningResource.objects.filter(pk=resource.pk).update(downloads_count=F('downloads_count') + 1)
        resource.refresh_from_db()
        return Response({'downloads_count': resource.downloads_count})
