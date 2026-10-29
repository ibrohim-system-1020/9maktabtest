from datetime import date, time, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.academics.models import (
    AcademicYear, Term, Subject, Classroom,
    TeacherProfile, StudentProfile, GuardianProfile,
    StudentGuardianRelation, TeacherClassSubject
)
from apps.timetables.models import TimetableEntry
from apps.attendance.models import AttendanceSession, AttendanceRecord
from apps.assignments.models import Assignment, AssignmentSubmission
from apps.assessments.models import Assessment, AssessmentResult
from apps.resources.models import LearningResource
from apps.portal.models import (
    SchoolInfo, Announcement, SchoolEvent,
    Achievement, GalleryItem, FAQ, PublicInquiry
)
from apps.notifications.models import Notification

User = get_user_model()

class Command(BaseCommand):
    help = "9-Maktab maktabi uchun to'liq namunaviy (demo) ma'lumotlarni yaratish"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("9-Maktab demo ma'lumotlarini yaratish boshlandi..."))

        # 1. School Info
        school, _ = SchoolInfo.objects.get_or_create(
            id=1,
            defaults={
                'name': "9-sonli umumiy o‘rta ta‘lim maktabi",
                'short_name': "9-Maktab",
                'region': "Toshkent shahri",
                'district': "Yunusobod tumani",
                'address': "Amir Temur shoh ko‘chasi, 45-uy",
                'phone': "+998 (71) 234-56-78",
                'email': "info@9maktab.uz",
                'director_name': "Abdullayev Rustam Karimovich",
                'founded_year': 1984,
                'hero_title': "Kelajak yetakchilarini tarbiyalovchi zamonaviy maktab",
                'hero_subtitle': "9-Maktab — raqamli innovatsiyalar, aniq fanlar va iqtidorli yoshlar maskani.",
                'mission': "Har bir o‘quvchining iqtidorini ro‘yobga chiqarish va milliy qadriyatlar asosida global raqobatbardosh bilim berish.",
                'vision': "O‘zbekistonning eng ilg‘or va nufuzli umumta'lim maktablaridan biriga aylanish."
            }
        )

        # 2. Users (Super admin, School admin, Principal, Teachers, Students, Guardians)
        def create_user(username, email, first_name, last_name, role, password="Password123!"):
            u, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role,
                    'is_staff': role in ['super_admin', 'school_admin'],
                    'is_superuser': role == 'super_admin',
                }
            )
            u.set_password(password)
            u.save()
            return u

        # Admins & Principal
        admin_user = create_user('admin', 'admin@9maktab.uz', 'Bosh', 'Administrator', 'super_admin')
        school_admin = create_user('school_admin', 'manager@9maktab.uz', 'Nozima', 'Qosimova', 'school_admin')
        principal = create_user('direktor', 'director@9maktab.uz', 'Rustam', 'Abdullayev', 'principal')

        # Teachers
        t_math = create_user('teacher_math', 'math@9maktab.uz', 'Nilufar', 'Sobirova', 'teacher')
        t_phys = create_user('teacher_physics', 'physics@9maktab.uz', 'Jamshid', 'Karimov', 'teacher')
        t_lang = create_user('teacher_lang', 'lang@9maktab.uz', 'Dilnoza', 'Mahmudova', 'teacher')
        t_cs = create_user('teacher_cs', 'cs@9maktab.uz', 'Azizbek', 'Yusupov', 'teacher')
        t_eng = create_user('teacher_eng', 'eng@9maktab.uz', 'Malika', 'Smitova', 'teacher')

        # Teacher Profiles
        tp_math, _ = TeacherProfile.objects.get_or_create(
            user=t_math,
            defaults={'employee_id': 'TCH-001', 'qualification': 'Oliy toifali o\'qituvchi', 'specialization': 'Matematika va Geometriya', 'room_number': '204'}
        )
        tp_phys, _ = TeacherProfile.objects.get_or_create(
            user=t_phys,
            defaults={'employee_id': 'TCH-002', 'qualification': '1-toifali o\'qituvchi', 'specialization': 'Fizika va Astronomiya', 'room_number': '108'}
        )
        tp_lang, _ = TeacherProfile.objects.get_or_create(
            user=t_lang,
            defaults={'employee_id': 'TCH-003', 'qualification': 'Oliy toifali o\'qituvchi', 'specialization': 'Ona tili va Adabiyot', 'room_number': '302'}
        )
        tp_cs, _ = TeacherProfile.objects.get_or_create(
            user=t_cs,
            defaults={'employee_id': 'TCH-004', 'qualification': '1-toifali o\'qituvchi', 'specialization': 'Informatika va IT', 'room_number': 'IT-Lab'}
        )
        tp_eng, _ = TeacherProfile.objects.get_or_create(
            user=t_eng,
            defaults={'employee_id': 'TCH-005', 'qualification': 'Oliy toifali o\'qituvchi (CEFR C1)', 'specialization': 'Ingliz tili', 'room_number': '210'}
        )

        # 3. Academic Year & Terms
        ay, _ = AcademicYear.objects.get_or_create(
            name='2026-2027',
            defaults={'start_date': date(2026, 9, 2), 'end_date': date(2027, 5, 25), 'is_current': True}
        )

        term1, _ = Term.objects.get_or_create(academic_year=ay, term_number=1, defaults={'name': '1-Chorak', 'start_date': date(2026, 9, 2), 'end_date': date(2026, 11, 4), 'is_current': False})
        term2, _ = Term.objects.get_or_create(academic_year=ay, term_number=2, defaults={'name': '2-Chorak', 'start_date': date(2026, 11, 11), 'end_date': date(2026, 12, 28), 'is_current': True})
        term3, _ = Term.objects.get_or_create(academic_year=ay, term_number=3, defaults={'name': '3-Chorak', 'start_date': date(2027, 1, 11), 'end_date': date(2027, 3, 20), 'is_current': False})
        term4, _ = Term.objects.get_or_create(academic_year=ay, term_number=4, defaults={'name': '4-Chorak', 'start_date': date(2027, 3, 29), 'end_date': date(2027, 5, 25), 'is_current': False})

        # 4. Subjects
        sub_math, _ = Subject.objects.get_or_create(code='MATH-09', defaults={'name': 'Algebra va Geometriya', 'category': 'exact', 'icon': 'Calculator'})
        sub_phys, _ = Subject.objects.get_or_create(code='PHYS-09', defaults={'name': 'Fizika', 'category': 'natural', 'icon': 'Zap'})
        sub_lang, _ = Subject.objects.get_or_create(code='UZB-09', defaults={'name': 'Ona tili va Adabiyot', 'category': 'languages', 'icon': 'BookOpen'})
        sub_cs, _ = Subject.objects.get_or_create(code='CS-09', defaults={'name': 'Informatika va IT', 'category': 'exact', 'icon': 'Laptop'})
        sub_eng, _ = Subject.objects.get_or_create(code='ENG-09', defaults={'name': 'Ingliz tili', 'category': 'languages', 'icon': 'Globe'})
        sub_chem, _ = Subject.objects.get_or_create(code='CHEM-09', defaults={'name': 'Kimyo', 'category': 'natural', 'icon': 'FlaskConical'})

        # 5. Classrooms
        c_9a, _ = Classroom.objects.get_or_create(grade_level=9, section='A', academic_year=ay, defaults={'name': '9-A', 'class_teacher': t_math, 'room_number': '204'})
        c_9b, _ = Classroom.objects.get_or_create(grade_level=9, section='B', academic_year=ay, defaults={'name': '9-B', 'class_teacher': t_phys, 'room_number': '108'})
        c_10a, _ = Classroom.objects.get_or_create(grade_level=10, section='A', academic_year=ay, defaults={'name': '10-A', 'class_teacher': t_cs, 'room_number': 'IT-Lab'})
        c_11a, _ = Classroom.objects.get_or_create(grade_level=11, section='A', academic_year=ay, defaults={'name': '11-A', 'class_teacher': t_lang, 'room_number': '302'})

        # Teacher Class Subject assignments
        TeacherClassSubject.objects.get_or_create(teacher=tp_math, classroom=c_9a, subject=sub_math, academic_year=ay, defaults={'weekly_hours': 5})
        TeacherClassSubject.objects.get_or_create(teacher=tp_phys, classroom=c_9a, subject=sub_phys, academic_year=ay, defaults={'weekly_hours': 3})
        TeacherClassSubject.objects.get_or_create(teacher=tp_lang, classroom=c_9a, subject=sub_lang, academic_year=ay, defaults={'weekly_hours': 4})
        TeacherClassSubject.objects.get_or_create(teacher=tp_cs, classroom=c_9a, subject=sub_cs, academic_year=ay, defaults={'weekly_hours': 2})
        TeacherClassSubject.objects.get_or_create(teacher=tp_eng, classroom=c_9a, subject=sub_eng, academic_year=ay, defaults={'weekly_hours': 3})

        TeacherClassSubject.objects.get_or_create(teacher=tp_math, classroom=c_9b, subject=sub_math, academic_year=ay, defaults={'weekly_hours': 5})
        TeacherClassSubject.objects.get_or_create(teacher=tp_phys, classroom=c_9b, subject=sub_phys, academic_year=ay, defaults={'weekly_hours': 3})

        # 6. Students
        students_data = [
            ('student_jasur', 'jasur@student.9maktab.uz', 'Jasur', 'Alimov', c_9a, '9M-2026-001', 'male', date(2011, 4, 15), '+998901112233'),
            ('student_madina', 'madina@student.9maktab.uz', 'Madina', 'Rustamova', c_9a, '9M-2026-002', 'female', date(2011, 8, 22), '+998902223344'),
            ('student_bobur', 'bobur@student.9maktab.uz', 'Bobur', 'Qodirov', c_9a, '9M-2026-003', 'male', date(2011, 1, 10), '+998903334455'),
            ('student_shaxzoda', 'shaxzoda@student.9maktab.uz', 'Shaxzoda', 'Karimova', c_9a, '9M-2026-004', 'female', date(2011, 6, 18), '+998904445566'),
            ('student_temur', 'temur@student.9maktab.uz', 'Temur', 'Umarov', c_9b, '9M-2026-005', 'male', date(2011, 9, 5), '+998905556677'),
            ('student_dilnoza', 'dilnoza@student.9maktab.uz', 'Dilnoza', 'Rahimova', c_10a, '9M-2026-006', 'female', date(2010, 3, 12), '+998906667788'),
        ]

        created_students = []
        for username, email, fn, ln, classroom, sid, gender, bdate, phone in students_data:
            u = create_user(username, email, fn, ln, 'student')
            sp, _ = StudentProfile.objects.get_or_create(
                user=u,
                defaults={
                    'classroom': classroom,
                    'student_id': sid,
                    'gender': gender,
                    'birth_date': bdate,
                    'parent_phone': phone,
                }
            )
            created_students.append(sp)

        # 7. Guardians
        p_alimov = create_user('parent_alimov', 'o.alimov@mail.uz', 'Otabek', 'Alimov', 'guardian')
        gp_alimov, _ = GuardianProfile.objects.get_or_create(user=p_alimov, defaults={'occupation': 'Muhandis', 'emergency_phone': '+998901112233'})
        StudentGuardianRelation.objects.get_or_create(student=created_students[0], guardian=gp_alimov, defaults={'relationship': 'father', 'is_primary': True, 'is_verified': True})

        p_rustamova = create_user('parent_rustamova', 'g.rustamova@mail.uz', 'Gulnora', 'Rustamova', 'guardian')
        gp_rustamova, _ = GuardianProfile.objects.get_or_create(user=p_rustamova, defaults={'occupation': 'Shifokor', 'emergency_phone': '+998902223344'})
        StudentGuardianRelation.objects.get_or_create(student=created_students[1], guardian=gp_rustamova, defaults={'relationship': 'mother', 'is_primary': True, 'is_verified': True})

        # 8. Timetable Entries for 9-A
        timetable_schedule = [
            # Monday (1)
            (1, 1, sub_math, tp_math, time(8, 30), time(9, 15), '204'),
            (1, 2, sub_math, tp_math, time(9, 25), time(10, 10), '204'),
            (1, 3, sub_phys, tp_phys, time(10, 30), time(11, 15), '108'),
            (1, 4, sub_lang, tp_lang, time(11, 25), time(12, 10), '302'),
            (1, 5, sub_eng, tp_eng, time(12, 20), time(13, 5), '210'),

            # Tuesday (2)
            (2, 1, sub_cs, tp_cs, time(8, 30), time(9, 15), 'IT-Lab'),
            (2, 2, sub_cs, tp_cs, time(9, 25), time(10, 10), 'IT-Lab'),
            (2, 3, sub_math, tp_math, time(10, 30), time(11, 15), '204'),
            (2, 4, sub_phys, tp_phys, time(11, 25), time(12, 10), '108'),

            # Wednesday (3)
            (3, 1, sub_lang, tp_lang, time(8, 30), time(9, 15), '302'),
            (3, 2, sub_lang, tp_lang, time(9, 25), time(10, 10), '302'),
            (3, 3, sub_eng, tp_eng, time(10, 30), time(11, 15), '210'),
            (3, 4, sub_math, tp_math, time(11, 25), time(12, 10), '204'),

            # Thursday (4)
            (4, 1, sub_phys, tp_phys, time(8, 30), time(9, 15), '108'),
            (4, 2, sub_math, tp_math, time(9, 25), time(10, 10), '204'),
            (4, 3, sub_eng, tp_eng, time(10, 30), time(11, 15), '210'),

            # Friday (5)
            (5, 1, sub_lang, tp_lang, time(8, 30), time(9, 15), '302'),
            (5, 2, sub_cs, tp_cs, time(9, 25), time(10, 10), 'IT-Lab'),
            (5, 3, sub_math, tp_math, time(10, 30), time(11, 15), '204'),
        ]

        for day, period, subj, teacher, st, et, room in timetable_schedule:
            TimetableEntry.objects.get_or_create(
                classroom=c_9a,
                academic_year=ay,
                day_of_week=day,
                period_number=period,
                defaults={
                    'subject': subj,
                    'teacher': teacher,
                    'term': term2,
                    'start_time': st,
                    'end_time': et,
                    'room_number': room,
                }
            )

        # 9. Attendance Sessions & Records (Past 10 school days)
        today = timezone.now().date()
        for i in range(10):
            day_date = today - timedelta(days=i)
            if day_date.weekday() >= 6:  # Skip Sunday
                continue
            session, _ = AttendanceSession.objects.get_or_create(
                classroom=c_9a,
                date=day_date,
                defaults={'term': term2, 'recorded_by': t_math}
            )
            # Create records for students
            for idx, student in enumerate(created_students[:4]):
                # Realistic distribution: mostly present, occasionally late or absent
                if i == 2 and idx == 2:
                    status_choice = 'absent'
                    reason = "Kasal bo'lganligi sababli"
                elif i == 4 and idx == 0:
                    status_choice = 'late'
                    reason = "Yo'l tirbandligi"
                else:
                    status_choice = 'present'
                    reason = ''
                AttendanceRecord.objects.get_or_create(
                    session=session,
                    student=student,
                    defaults={'status': status_choice, 'reason': reason}
                )

        # 10. Assignments & Submissions
        assign1, _ = Assignment.objects.get_or_create(
            classroom=c_9a,
            subject=sub_math,
            title="Kvadrat tenglamalar va Viyet teoremasi",
            defaults={
                'teacher': tp_math,
                'term': term2,
                'description': "Darslikdagi 142-148-misollarni yechish va daftarga yozib tushuntirish berish.",
                'max_score': 100,
                'due_date': timezone.now() + timedelta(days=3),
                'is_published': True,
            }
        )
        assign2, _ = Assignment.objects.get_or_create(
            classroom=c_9a,
            subject=sub_phys,
            title="Nyuton qonunlari va harakat dinamikasi",
            defaults={
                'teacher': tp_phys,
                'term': term2,
                'description': "Laboratoriya ishi hisoboti va 5 ta masala yechimi.",
                'max_score': 100,
                'due_date': timezone.now() + timedelta(days=5),
                'is_published': True,
            }
        )

        # Student submissions
        subm1, _ = AssignmentSubmission.objects.get_or_create(
            assignment=assign1,
            student=created_students[0],  # Jasur
            defaults={
                'submission_text': "Misollar to'liq yechildi. Viyet teoremasi orqali ildizlar tekshirildi.",
                'status': 'graded',
                'score': 95.0,
                'feedback': "A'lo darajada bajarilgan, hisoblashlar aniq!",
                'graded_by': t_math,
                'graded_at': timezone.now(),
            }
        )
        subm2, _ = AssignmentSubmission.objects.get_or_create(
            assignment=assign1,
            student=created_students[1],  # Madina
            defaults={
                'submission_text': "Barcha topshiriqlar daftarda bajarildi.",
                'status': 'graded',
                'score': 88.0,
                'feedback': "Juda yaxshi, 146-misolda kichik noaniqlik bor.",
                'graded_by': t_math,
                'graded_at': timezone.now(),
            }
        )

        # 11. Assessments & Results (BSB & CHSB)
        ass1, _ = Assessment.objects.get_or_create(
            classroom=c_9a,
            subject=sub_math,
            title="1-BSB: Kvadrat tenglamalar nazorat ishi",
            defaults={
                'teacher': tp_math,
                'term': term2,
                'assessment_type': 'quiz',
                'date': today - timedelta(days=7),
                'max_score': 100.0,
                'weight': 1.0,
            }
        )
        AssessmentResult.objects.get_or_create(assessment=ass1, student=created_students[0], defaults={'score': 95.0, 'grade_number': 5, 'remarks': "A'lo bilim"})
        AssessmentResult.objects.get_or_create(assessment=ass1, student=created_students[1], defaults={'score': 86.0, 'grade_number': 5, 'remarks': "Yaxshi natija"})
        AssessmentResult.objects.get_or_create(assessment=ass1, student=created_students[2], defaults={'score': 74.0, 'grade_number': 4, 'remarks': "Qoniqarli"})
        AssessmentResult.objects.get_or_create(assessment=ass1, student=created_students[3], defaults={'score': 82.0, 'grade_number': 4, 'remarks': "Yaxshi natija"})

        # 12. Learning Resources
        LearningResource.objects.get_or_create(
            title="9-sinf Algebra elektron darsligi va metodik qo‘llanma",
            subject=sub_math,
            defaults={
                'grade_level': 9,
                'file_type': 'pdf',
                'resource_url': 'https://storage.9maktab.uz/resources/algebra_9_sinf.pdf',
                'file_size_mb': 14.2,
                'uploaded_by': t_math,
                'downloads_count': 142,
                'is_public': True,
            }
        )
        LearningResource.objects.get_or_create(
            title="Fizika: Dinamika qonunlari interaktiv slaydlar",
            subject=sub_phys,
            defaults={
                'grade_level': 9,
                'file_type': 'presentation',
                'resource_url': 'https://storage.9maktab.uz/resources/fizika_dinamika.pptx',
                'file_size_mb': 8.5,
                'uploaded_by': t_phys,
                'downloads_count': 89,
                'is_public': True,
            }
        )

        # 13. Announcements
        Announcement.objects.get_or_create(
            slug='respublika-fan-olimpiadasi-2026',
            defaults={
                'title': "Respublika fan olimpiadasining tuman bosqichi o‘tkaziladi",
                'summary': "Joriy yilning 15-noyabr kuni maktabimizda aniq va tabiiy fanlar bo‘yicha tuman olimpiadasi bo‘lib o‘tadi.",
                'content': "Olimpiadada 9-11-sinf o'quvchilari ishtirok etishlari mumkin. Barcha ishtirokchilarga omad tilaymiz!",
                'category': 'academic',
                'target_role': 'all',
                'is_pinned': True,
                'is_published': True,
                'views_count': 324,
                'author': school_admin,
            }
        )
        Announcement.objects.get_or_create(
            slug='ota-onalar-majlis-rejasi',
            defaults={
                'title': "1-chorak yakunlari bo‘yicha ota-onalar majlisi",
                'summary': "O‘quvchilarning 1-chorakdagi o‘zlashtirish ko‘rsatkichlari va davomati muhokama qilinadi.",
                'content': "Hurmatli ota-onalar! Sizlarni juma kuni soat 17:00 da farzandingiz sinf xonasida kutamiz.",
                'category': 'general',
                'target_role': 'guardians',
                'is_pinned': False,
                'is_published': True,
                'views_count': 185,
                'author': school_admin,
            }
        )

        # 14. Events
        SchoolEvent.objects.get_or_create(
            title="Yosh dasturchilar va Robototexnika festivali",
            event_date=today + timedelta(days=6),
            defaults={
                'description': "Maktabimiz o‘quvchilari tomonidan tayyorlangan robotlar va dasturiy loyihalar ko‘rgazmasi.",
                'start_time': time(10, 0),
                'end_time': time(13, 0),
                'location': "Maktab faollar zali",
                'organizer': "Informatika va IT fani to‘garagi",
                'is_public': True,
            }
        )
        SchoolEvent.objects.get_or_create(
            title="Zakovat intellektual turniri (Kuzgi mavsum)",
            event_date=today + timedelta(days=12),
            defaults={
                'description': "Sinflararo an'anaviy Zakovat bellashuvining final bosqichi.",
                'start_time': time(14, 0),
                'end_time': time(16, 30),
                'location': "Axborot-resurs markazi",
                'organizer': "Yoshlar ittifoqi yetakchisi",
                'is_public': True,
            }
        )

        # 15. Achievements
        Achievement.objects.get_or_create(
            title="Xalqaro Matematika Olimpiadasi (IMO) Bronza medali",
            winner_name="Jasur Alimov",
            defaults={
                'category': 'olympiad',
                'grade_or_role': "9-A sinf o‘quvchisi",
                'description': "Xalqaro matematika olimpiadasida 9-maktab o‘quvchisi faxrli 3-o‘rinni egalladi.",
                'date': date(2026, 7, 20),
                'badge_icon': 'Award',
            }
        )
        Achievement.objects.get_or_create(
            title="Toshkent shahar maktablararo voleybol chempionati 1-o‘rin",
            winner_name="9-Maktab o‘g‘il bolalar terma jamoasi",
            defaults={
                'category': 'sports',
                'grade_or_role': "Sport to‘garagi",
                'description': "Shahardagi 120 dan ortiq maktablar orasida jamoamiz mutlaq chempion bo‘ldi.",
                'date': date(2026, 5, 14),
                'badge_icon': 'Trophy',
            }
        )

        # 16. FAQs
        FAQ.objects.get_or_create(
            question="9-Maktabga o‘qishga qabul qilish tartibi qanday?",
            defaults={
                'answer': "1-sinfga qabul davlat xizmatlari portali (my.maktab.uz) orqali mikrohudud va mikrohududdan tashqari bosqichlar asosida amalga oshiriladi.",
                'category': "Qabul jarayoni",
                'order': 1,
            }
        )
        FAQ.objects.get_or_create(
            question="Maktabda qanday qo‘shimcha to‘garaklar mavjud?",
            defaults={
                'answer': "Maktabimizda Robototexnika, Mental arifmetika, Shaxmat, Zakovat klubi, Ingliz tili (IELTS), Voleybol va Basketbol to‘garaklari bepul faoliyat yuritadi.",
                'category': "O‘quv jarayoni",
                'order': 2,
            }
        )

        # 17. Public Inquiry
        PublicInquiry.objects.get_or_create(
            email='vali.karimov@gmail.com',
            subject="Farzandimni 9-sinfga ko'chirish bo'yicha",
            defaults={
                'full_name': "Vali Karimov",
                'phone': "+998 90 777 88 99",
                'message': "Assalomu alaykum! Boshqa viloyatdan Toshkent shahriga ko'chib keldik. 9-sinfga qabul qilish uchun qanday hujjatlar kerak bo'ladi?",
                'status': 'resolved',
                'admin_response': "Vaalaykum assalom! Maktab ma'muriyatiga o'quvchining shaxsiy yig'majildi va yashash joyi ma'lumotnomasi bilan murojaat qilishingiz mumkin.",
            }
        )

        # 18. Notifications
        Notification.objects.get_or_create(
            recipient=created_students[0].user,
            title="Yangi vazifa baholandi",
            defaults={
                'message': "Algebra fanidan 'Kvadrat tenglamalar' vazifangiz 95 ball bilan baholandi.",
                'notification_type': 'grade',
                'is_read': False,
            }
        )

        self.stdout.write(self.style.SUCCESS("✓ 9-Maktab barcha namunaviy ma'lumotlari muvaffaqiyatli yaratildi!"))
        self.stdout.write(self.style.SUCCESS("""
Test akkauntlari:
- Super Administrator: admin / Password123!
- Maktab Administratori: school_admin / Password123!
- Direktor: direktor / Password123!
- O'qituvchi (Matematika): teacher_math / Password123!
- O'quvchi (9-A): student_jasur / Password123!
- Ota-ona: parent_alimov / Password123!
        """))
