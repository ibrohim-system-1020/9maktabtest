from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.resources.views import LearningResourceViewSet

router = DefaultRouter()
router.register(r'resources', LearningResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
