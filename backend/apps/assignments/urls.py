from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.assignments.views import AssignmentViewSet, AssignmentSubmissionViewSet

router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', AssignmentSubmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
