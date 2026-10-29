from rest_framework import viewsets
from apps.audit.models import AuditLog
from apps.audit.serializers import AuditLogSerializer
from apps.accounts.permissions import IsSchoolAdminUser

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user').all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    permission_classes = [IsSchoolAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        action_filter = self.request.query_params.get('action')
        model_name = self.request.query_params.get('model_name')
        if action_filter:
            queryset = queryset.filter(action=action_filter)
        if model_name:
            queryset = queryset.filter(model_name__icontains=model_name)
        return queryset
