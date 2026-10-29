from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.academics.models import (
    AcademicYear, Term, Subject, Classroom,
    StudentProfile, TeacherProfile, GuardianProfile,
    StudentGuardianRelation, TeacherClassSubject
)
from apps.attendance.models import AttendanceSession, AttendanceRecord
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.assessments.models import Assessment, AssessmentResult
from apps.analytics.services import AnalyticsEngine

User = get_user_model()

class SchoolPlatformTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Admin
        self.admin = User.objects.create_superuser(
            username='test_admin',
            email='admin@test.com',
            password='Password123!',
            role='school_admin'
        )

        # Create Teacher
        self.teacher_user = User.objects.create_user(
            username='test_teacher',
            email='teacher@test.com',
            password='Password123!',
            role='teacher',
            first_name='Zuhra',
            last_name='Nazarova'
        )
        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher_user,
            employee_id='TCH-TEST-1',
            specialization='Matematika'
        )

        # Create Student 1
        self.student1_user = User.objects.create_user(
            username='test_student1',
            email='student1@test.com',
            password='Password123!',
            role='student',
            first_name='Anvar',
            last_name='Toshmatov'
        )
        self.student1_profile = StudentProfile.objects.create(
            user=self.student1_user,
            student_id='STU-TEST-1'
        )

        # Create Student 2
        self.student2_user = User.objects.create_user(
            username='test_student2',
            email='student2@test.com',
            password='Password123!',
            role='student',
            first_name='Barno',
            last_name='Eshmatova'
        )
        self.student2_profile = StudentProfile.objects.create(
            user=self.student2_user,
            student_id='STU-TEST-2'
        )

        # Academic structure
        self.year = AcademicYear.objects.create(name='2026-2027', start_date='2026-09-01', end_date='2027-05-25', is_current=True)
        self.term = Term.objects.create(academic_year=self.year, name='1-Chorak', term_number=1, start_date='2026-09-01', end_date='2026-11-04', is_current=True)
        self.subject = Subject.objects.create(name='Matematika', code='MATH-T', category='exact')
        self.classroom = Classroom.objects.create(grade_level=9, section='A', name='9-A', academic_year=self.year, class_teacher=self.teacher_user)

        self.student1_profile.classroom = self.classroom
        self.student1_profile.save()
        self.student2_profile.classroom = self.classroom
        self.student2_profile.save()

        # Assign teacher
        TeacherClassSubject.objects.create(
            teacher=self.teacher_profile,
            classroom=self.classroom,
            subject=self.subject,
            academic_year=self.year,
            weekly_hours=4
        )

    def test_health_check_endpoint(self):
        """Test system health check returns 200 OK and status healthy"""
        res = self.client.get('/health/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['status'], 'healthy')

        res_api = self.client.get('/api/health/')
        self.assertEqual(res_api.status_code, status.HTTP_200_OK)

    def test_jwt_authentication(self):
        """Test login gives JWT token and user profile"""
        res = self.client.post('/api/auth/token/', {
            'username': 'test_teacher',
            'password': 'Password123!'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)
        self.assertEqual(res.data['user']['role'], 'teacher')

    def test_student_data_isolation(self):
        """Test that a student cannot view other students' profiles"""
        self.client.force_authenticate(user=self.student1_user)
        res = self.client.get('/api/academics/students/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Student should only see 1 record: themselves
        results = res.data if isinstance(res.data, list) else res.data.get('results', [])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['student_id'], 'STU-TEST-1')

    def test_attendance_formula_and_recording(self):
        """Test attendance bulk save and calculated rate: (present + late) / total * 100"""
        self.client.force_authenticate(user=self.teacher_user)
        post_data = {
            'classroom_id': self.classroom.id,
            'date': '2026-10-25',
            'term_id': self.term.id,
            'records': [
                {'student_id': self.student1_profile.id, 'status': 'present', 'reason': ''},
                {'student_id': self.student2_profile.id, 'status': 'absent', 'reason': 'Kasal'}
            ]
        }
        res = self.client.post('/api/attendance/sessions/save_bulk/', post_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify session and records in DB
        session = AttendanceSession.objects.get(classroom=self.classroom, date='2026-10-25')
        self.assertEqual(session.records.count(), 2)

        # Check analytics formula
        analytics = AnalyticsEngine.get_attendance_analytics(classroom_id=self.classroom.id)
        # 1 present, 1 absent -> (1/2) * 100 = 50.0%
        self.assertEqual(analytics['attendance_rate'], 50.0)

    def test_assignment_lifecycle(self):
        """Test teacher creates assignment, student submits, teacher grades"""
        # 1. Teacher creates assignment
        self.client.force_authenticate(user=self.teacher_user)
        res_create = self.client.post('/api/assignments/assignments/', {
            'classroom': self.classroom.id,
            'subject': self.subject.id,
            'title': 'Test Matematika Uy ishi',
            'description': '1-10 misollar',
            'due_date': '2026-11-15T18:00:00Z',
            'max_score': 100,
        }, format='json')
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        assignment_id = res_create.data['id']

        # 2. Student submits homework
        self.client.force_authenticate(user=self.student1_user)
        res_submit = self.client.post('/api/assignments/submissions/', {
            'assignment': assignment_id,
            'submission_text': 'Javoblar: 1) A, 2) B, 3) C',
        }, format='json')
        self.assertEqual(res_submit.status_code, status.HTTP_201_CREATED)
        submission_id = res_submit.data['id']

        # 3. Teacher grades submission
        self.client.force_authenticate(user=self.teacher_user)
        res_grade = self.client.post(f'/api/assignments/submissions/{submission_id}/grade/', {
            'score': 92.5,
            'feedback': 'Barakalla, to\'g\'ri yechilgan!'
        }, format='json')
        self.assertEqual(res_grade.status_code, status.HTTP_200_OK)

        # Verify in DB
        sub = AssignmentSubmission.objects.get(id=submission_id)
        self.assertEqual(sub.status, 'graded')
        self.assertEqual(float(sub.score), 92.5)

    def test_public_inquiry_workflow(self):
        """Test public visitor can submit inquiry and admin can respond"""
        # Anonymous visitor posts inquiry
        self.client.logout()
        res = self.client.post('/api/school/inquiries/', {
            'full_name': 'Akrom Aliyev',
            'email': 'akrom@gmail.com',
            'phone': '+998901234567',
            'subject': 'Kutubxona faoliyati',
            'message': 'Maktab kutubxonasi shanba kunlari ishlaydimi?'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        inquiry_id = res.data['id']

        # Admin responds
        self.client.force_authenticate(user=self.admin)
        res_reply = self.client.post(f'/api/school/inquiries/{inquiry_id}/respond/', {
            'admin_response': 'Ha, shanba kuni soat 9:00 dan 15:00 gacha ochiq.',
            'status': 'resolved'
        }, format='json')
        self.assertEqual(res_reply.status_code, status.HTTP_200_OK)
        self.assertEqual(res_reply.data['status'], 'resolved')
