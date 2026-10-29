from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.portal.views import (
    SchoolInfoView, AnnouncementViewSet, SchoolEventViewSet,
    AchievementViewSet, GalleryItemViewSet, FAQViewSet,
    PublicInquiryViewSet
)

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet)
router.register(r'events', SchoolEventViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'gallery', GalleryItemViewSet)
router.register(r'faq', FAQViewSet)
router.register(r'inquiries', PublicInquiryViewSet)

urlpatterns = [
    path('info/', SchoolInfoView.as_view(), name='school_info'),
    path('', include(router.urls)),
]
