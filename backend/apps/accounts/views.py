from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db import models, transaction
from apps.accounts.serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserCreateSerializer,
    ChangePasswordSerializer,
    StudentRegisterSerializer,
    GuardianRegisterSerializer
)
from apps.accounts.permissions import IsSchoolAdminUser
from apps.academics.models import Classroom, StudentProfile, GuardianProfile, StudentGuardianRelation
from apps.audit.models import AuditLog

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': ["Eski parol noto'g'ri kiritildi."]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    """
    Public registration endpoint strictly allowing only 'student' or 'guardian' roles.
    Admins/Teachers CANNOT be created here.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        account_type = request.data.get('account_type')
        if account_type not in ['student', 'guardian']:
            return Response(
                {'error': "Iltimos, hisob turini tanlang: 'student' (O'quvchi) yoki 'guardian' (Ota-ona)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if account_type == 'student':
            serializer = StudentRegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            classroom_id = data['classroom_id']
            student_id_code = data['student_id_code'].strip().upper()

            try:
                classroom = Classroom.objects.get(id=classroom_id)
            except Classroom.DoesNotExist:
                return Response({'classroom_id': ["Ko'rsatilgan sinf topilmadi."]}, status=status.HTTP_400_BAD_REQUEST)

            # Check if student_id is already assigned to another user
            if StudentProfile.objects.filter(student_id=student_id_code).exists():
                return Response(
                    {'student_id_code': [f"'{student_id_code}' ID raqamli o'quvchi allaqachon ro'yxatdan o'tgan."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                user = User.objects.create_user(
                    username=data['username'].strip(),
                    email=data.get('email', ''),
                    password=data['password'],
                    first_name=data['first_name'].strip(),
                    last_name=data['last_name'].strip(),
                    phone_number=data.get('phone_number', ''),
                    role=User.ROLE_STUDENT,
                    is_verified=True
                )
                student_profile = StudentProfile.objects.create(
                    user=user,
                    classroom=classroom,
                    student_id=student_id_code
                )
                AuditLog.objects.create(
                    user=user,
                    action='create',
                    model_name='User:StudentRegister',
                    object_id=str(user.id),
                    details=f"Yangi o'quvchi ro'yxatdan o'tdi: {user.get_full_name()} ({classroom.name}, ID: {student_id_code})"
                )

            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username
            refresh['role'] = user.role
            refresh['full_name'] = user.get_full_name()

            return Response({
                'message': "O'quvchi hisobi muvaffaqiyatli yaratildi!",
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

        elif account_type == 'guardian':
            serializer = GuardianRegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            data = serializer.validated_data
            child_id = data['child_student_id'].strip().upper()

            # Verify child exists in the school database
            child_student = StudentProfile.objects.filter(student_id=child_id).first()
            if not child_student:
                return Response(
                    {'child_student_id': [f"'{child_id}' ID raqamli o'quvchi maktab bazasidan topilmadi. Iltimos, farzandingizning to'g'ri o'quvchi ID raqamini kiriting (masalan: 9M-2026-001)."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                user = User.objects.create_user(
                    username=data['username'].strip(),
                    email=data.get('email', ''),
                    password=data['password'],
                    first_name=data['first_name'].strip(),
                    last_name=data['last_name'].strip(),
                    phone_number=data['phone_number'].strip(),
                    role=User.ROLE_GUARDIAN,
                    is_verified=True
                )
                guardian_profile = GuardianProfile.objects.create(
                    user=user,
                    emergency_phone=data['phone_number'].strip()
                )
                relation = StudentGuardianRelation.objects.create(
                    student=child_student,
                    guardian=guardian_profile,
                    relationship=data.get('relationship', 'father'),
                    is_primary=True,
                    is_verified=True
                )
                AuditLog.objects.create(
                    user=user,
                    action='create',
                    model_name='User:GuardianRegister',
                    object_id=str(user.id),
                    details=f"Yangi ota-ona ro'yxatdan o'tdi: {user.get_full_name()} -> Farzandi: {child_student.user.get_full_name()} ({child_student.student_id})"
                )

            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username
            refresh['role'] = user.role
            refresh['full_name'] = user.get_full_name()

            return Response({
                'message': f"Ota-ona hisobi muvaffaqiyatli yaratildi va {child_student.user.get_full_name()} profiliga bog'landi!",
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsSchoolAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role')
        search = self.request.query_params.get('search')
        if role:
            queryset = queryset.filter(role=role)
        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(username__icontains=search) |
                models.Q(phone_number__icontains=search)
            )
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[IsSchoolAdminUser])
    def toggle_active(self, request, pk=None):
        target_user = self.get_object()
        target_user.is_active = not target_user.is_active
        target_user.save()
        status_text = "faollashtirildi" if target_user.is_active else "faolsizlantirildi"
        AuditLog.objects.create(
            user=request.user,
            action='update',
            model_name='User',
            object_id=str(target_user.id),
            details=f"Foydalanuvchi {target_user.username} {status_text}."
        )
        return Response({'is_active': target_user.is_active, 'message': f"Foydalanuvchi {status_text}."})

    @action(detail=True, methods=['post'], permission_classes=[IsSchoolAdminUser])
    def reset_password(self, request, pk=None):
        target_user = self.get_object()
        new_password = request.data.get('new_password')
        if not new_password or len(new_password) < 6:
            return Response({'error': "Yangi parol kamida 6 belgidan iborat bo'lishi kerak."}, status=status.HTTP_400_BAD_REQUEST)
        target_user.set_password(new_password)
        target_user.save()
        AuditLog.objects.create(
            user=request.user,
            action='update',
            model_name='User',
            object_id=str(target_user.id),
            details=f"Foydalanuvchi {target_user.username} paroli admin tomonidan yangilandi."
        )
        return Response({'message': f"Foydalanuvchi {target_user.username} paroli muvaffaqiyatli yangilandi."})
