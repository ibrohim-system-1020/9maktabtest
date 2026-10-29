from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F, Q
from django.utils import timezone
from apps.portal.models import (
    SchoolInfo, Announcement, SchoolEvent,
    Achievement, GalleryItem, FAQ, PublicInquiry
)
from apps.portal.serializers import (
    SchoolInfoSerializer, AnnouncementSerializer,
    SchoolEventSerializer, AchievementSerializer,
    GalleryItemSerializer, FAQSerializer,
    PublicInquirySerializer, PublicInquiryAdminSerializer
)
from apps.accounts.permissions import IsSchoolAdminUser, ReadOnlyOrAdmin
from apps.audit.models import AuditLog

class SchoolInfoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        info = SchoolInfo.objects.first()
        if not info:
            info = SchoolInfo.objects.create()
        return Response(SchoolInfoSerializer(info).data)

    def put(self, request):
        if not (request.user and request.user.is_authenticated and request.user.is_school_admin):
            return Response({'error': "Faqat maktab administratori o‘zgartira oladi."}, status=status.HTTP_403_FORBIDDEN)
        info = SchoolInfo.objects.first()
        if not info:
            info = SchoolInfo.objects.create()
        serializer = SchoolInfoSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('author').all()
    serializer_class = AnnouncementSerializer
    permission_classes = [ReadOnlyOrAdmin]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if not (user and user.is_authenticated and user.is_school_admin):
            queryset = queryset.filter(is_published=True)
            if not (user and user.is_authenticated):
                queryset = queryset.filter(target_role__in=['all'])
            elif user.is_student_user:
                queryset = queryset.filter(target_role__in=['all', 'students'])
            elif user.is_teacher_user:
                queryset = queryset.filter(target_role__in=['all', 'teachers'])
            elif user.is_guardian_user:
                queryset = queryset.filter(target_role__in=['all', 'guardians'])

        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def view(self, request, pk=None):
        announcement = self.get_object()
        Announcement.objects.filter(pk=announcement.pk).update(views_count=F('views_count') + 1)
        announcement.refresh_from_db()
        return Response({'views_count': announcement.views_count})

class SchoolEventViewSet(viewsets.ModelViewSet):
    queryset = SchoolEvent.objects.all()
    serializer_class = SchoolEventSerializer
    permission_classes = [ReadOnlyOrAdmin]

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [ReadOnlyOrAdmin]

class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
    permission_classes = [ReadOnlyOrAdmin]

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [ReadOnlyOrAdmin]

class PublicInquiryViewSet(viewsets.ModelViewSet):
    queryset = PublicInquiry.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_school_admin:
            return PublicInquiryAdminSerializer
        return PublicInquirySerializer

    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated and user.is_school_admin:
            return super().get_queryset()
        # Non-admins cannot list inquiries
        return PublicInquiry.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[IsSchoolAdminUser])
    def respond(self, request, pk=None):
        inquiry = self.get_object()
        response_text = request.data.get('admin_response')
        new_status = request.data.get('status', 'resolved')

        if not response_text:
            return Response({'error': "Javob matni kiritilishi shart."}, status=status.HTTP_400_BAD_REQUEST)

        inquiry.admin_response = response_text
        inquiry.status = new_status
        inquiry.resolved_at = timezone.now()
        inquiry.save()

        return Response(PublicInquiryAdminSerializer(inquiry).data)
