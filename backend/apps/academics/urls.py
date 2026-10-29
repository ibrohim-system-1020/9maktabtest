from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.academics.views import (
    AcademicYearViewSet, TermViewSet, SubjectViewSet,
    ClassroomViewSet, StudentProfileViewSet,
    TeacherProfileViewSet, GuardianProfileViewSet,
    TeacherClassSubjectViewSet
)

router = DefaultRouter()
router.register(r'years', AcademicYearViewSet)
router.register(r'terms', TermViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'teachers', TeacherProfileViewSet)
router.register(r'guardians', GuardianProfileViewSet)
router.register(r'teacher-assignments', TeacherClassSubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
