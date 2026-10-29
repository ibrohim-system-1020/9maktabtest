from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.assessments.views import AssessmentViewSet, AssessmentResultViewSet

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet)
router.register(r'results', AssessmentResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
