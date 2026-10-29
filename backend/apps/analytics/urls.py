from django.urls import path
from apps.analytics.views import (
    SchoolOverviewAnalyticsView,
    AttendanceAnalyticsView,
    AcademicAnalyticsView,
    TeacherOperationalAnalyticsView,
    EngagementAnalyticsView,
    ExportAttendanceCSVView,
    ExportAcademicCSVView,
    ExportStudentsCSVView,
)

urlpatterns = [
    path('overview/', SchoolOverviewAnalyticsView.as_view(), name='analytics_overview'),
    path('attendance/', AttendanceAnalyticsView.as_view(), name='analytics_attendance'),
    path('academic/', AcademicAnalyticsView.as_view(), name='analytics_academic'),
    path('teachers/', TeacherOperationalAnalyticsView.as_view(), name='analytics_teachers'),
    path('engagement/', EngagementAnalyticsView.as_view(), name='analytics_engagement'),
    path('export/attendance/', ExportAttendanceCSVView.as_view(), name='export_attendance_csv'),
    path('export/academic/', ExportAcademicCSVView.as_view(), name='export_academic_csv'),
    path('export/students/', ExportStudentsCSVView.as_view(), name='export_students_csv'),
]
