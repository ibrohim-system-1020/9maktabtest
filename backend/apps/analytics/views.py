import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.analytics.services import AnalyticsEngine
from apps.attendance.models import AttendanceRecord
from apps.assessments.models import AssessmentResult
from apps.academics.models import StudentProfile
from apps.accounts.permissions import IsSchoolAdminUser, IsTeacherOrAdmin
from apps.audit.models import AuditLog

class SchoolOverviewAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = AnalyticsEngine.get_school_overview()
        return Response(data)

class AttendanceAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        classroom_id = request.query_params.get('classroom')
        days = int(request.query_params.get('days', 14))
        data = AnalyticsEngine.get_attendance_analytics(classroom_id=classroom_id, days=days)
        return Response(data)

class AcademicAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        classroom_id = request.query_params.get('classroom')
        subject_id = request.query_params.get('subject')
        data = AnalyticsEngine.get_academic_analytics(classroom_id=classroom_id, subject_id=subject_id)
        return Response(data)

class TeacherOperationalAnalyticsView(APIView):
    permission_classes = [IsSchoolAdminUser]

    def get(self, request):
        data = AnalyticsEngine.get_teacher_operational_analytics()
        return Response(data)

class EngagementAnalyticsView(APIView):
    permission_classes = [IsSchoolAdminUser]

    def get(self, request):
        data = AnalyticsEngine.get_engagement_analytics()
        return Response(data)

class ExportAttendanceCSVView(APIView):
    permission_classes = [IsTeacherOrAdmin]

    def get(self, request):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="davomat_hisoboti.csv"'

        writer = csv.writer(response)
        writer.writerow(['Sana', 'Sinf', 'O\'quvchi ID', 'O\'quvchi F.I.Sh.', 'Holat', 'Sabab'])

        records = AttendanceRecord.objects.select_related('session__classroom', 'student__user').all().order_by('-session__date')
        classroom_id = request.query_params.get('classroom')
        if classroom_id:
            records = records.filter(session__classroom_id=classroom_id)

        for r in records[:500]:
            writer.writerow([
                r.session.date,
                r.session.classroom.name,
                r.student.student_id,
                r.student.user.get_full_name(),
                r.get_status_display(),
                r.reason or ''
            ])

        AuditLog.objects.create(
            user=request.user,
            action='export_csv',
            model_name='AttendanceRecord',
            details="Davomat hisoboti CSV formatida yuklandi."
        )

        return response

class ExportAcademicCSVView(APIView):
    permission_classes = [IsTeacherOrAdmin]

    def get(self, request):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="baholar_hisoboti.csv"'

        writer = csv.writer(response)
        writer.writerow(['Sana', 'Sinf', 'Fan', 'O\'quvchi F.I.Sh.', 'Sinov turi', 'Ball', 'Baho (1-5)', 'Izoh'])

        results = AssessmentResult.objects.select_related('assessment__classroom', 'assessment__subject', 'student__user').all().order_by('-assessment__date')
        classroom_id = request.query_params.get('classroom')
        subject_id = request.query_params.get('subject')

        if classroom_id:
            results = results.filter(assessment__classroom_id=classroom_id)
        if subject_id:
            results = results.filter(assessment__subject_id=subject_id)

        for res in results[:500]:
            writer.writerow([
                res.assessment.date,
                res.assessment.classroom.name,
                res.assessment.subject.name,
                res.student.user.get_full_name(),
                res.assessment.get_assessment_type_display(),
                res.score,
                res.grade_number,
                res.remarks or ''
            ])

        AuditLog.objects.create(
            user=request.user,
            action='export_csv',
            model_name='AssessmentResult',
            details="Baholar hisoboti CSV formatida yuklandi."
        )

        return response

class ExportStudentsCSVView(APIView):
    permission_classes = [IsSchoolAdminUser]

    def get(self, request):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="oquvchilar_royxati.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID kodi', 'F.I.Sh.', 'Sinf', 'Tug\'ilgan sana', 'Jinsi', 'Telefon', 'Yashash manzili'])

        students = StudentProfile.objects.select_related('user', 'classroom').all().order_by('classroom__name', 'user__last_name')
        for s in students:
            writer.writerow([
                s.student_id,
                s.user.get_full_name(),
                s.classroom.name if s.classroom else '',
                s.birth_date or '',
                s.get_gender_display(),
                s.parent_phone or s.user.phone_number or '',
                s.user.address or ''
            ])

        AuditLog.objects.create(
            user=request.user,
            action='export_csv',
            model_name='StudentProfile',
            details="O'quvchilar ro'yxati CSV formatida yuklandi."
        )

        return response
