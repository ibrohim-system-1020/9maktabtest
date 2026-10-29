from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.timetables.views import TimetableEntryViewSet

router = DefaultRouter()
router.register(r'entries', TimetableEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
