from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.attendance.views import AttendanceSessionViewSet, AttendanceRecordViewSet

router = DefaultRouter()
router.register(r'sessions', AttendanceSessionViewSet)
router.register(r'records', AttendanceRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
