from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models

# 🔧 사용자 생성 및 관리 커스텀 매니저
class UserManager(BaseUserManager):
    # 일반 사용자 생성
    def create_user(self, email=None, password=None, **extra_fields):
        # 이메일이나 소셜 ID 하나는 반드시 있어야 함
        if not email and not extra_fields.get("kakao_user_id") and not extra_fields.get("naver_user_id"):
            raise ValueError("The user must have either email or a social ID.")
        
        # 이메일 존재 시 정규화
        email = self.normalize_email(email) if email else None
        # 유저 인스턴스 생성
        user = self.model(email=email, **extra_fields)

        # 비밀번호 설정 (없으면 사용 불가능한 비밀번호로 처리)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        
        user.save(using=self._db)
        return user

    # 슈퍼유저 생성 (관리자 계정)
    def create_superuser(self, email, password, **extra_fields):
        # 관리자 필수 권한 설정
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError("Superuser must have an email address")
        if not password:
            raise ValueError("Superuser must have a password")

        return self.create_user(email=email, password=password, **extra_fields)


# 👤 사용자 모델 정의 (AbstractBaseUser를 상속받아 커스텀 사용자 모델 구현)
class User(AbstractBaseUser, PermissionsMixin):
    # 🔹 사용자 기본 정보
    name = models.CharField(max_length=150, null=True, blank=True)  # 실명 또는 닉네임
    email = models.EmailField(unique=True, null=True, blank=True)  # 이메일 로그인용 (선택적)
    
    # 🔹 소셜 로그인 ID
    kakao_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # 카카오 계정 식별자
    naver_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)  # 네이버 계정 식별자

    # 🔹 사용자 상태 및 권한
    is_active = models.BooleanField(default=True)  # 활성 계정 여부
    is_staff = models.BooleanField(default=False)  # 관리자 페이지 접속 가능 여부

    # 🔹 그룹 및 권한 (Django 기본 그룹/권한 시스템 연동)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    # 🔹 사용자 객체 생성 매니저 등록
    objects = UserManager()

    # 🔹 인증에 사용할 필드 설정 (기본은 email)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # createsuperuser 시 필수 입력 항목 (email은 USERNAME_FIELD에 포함되어 있으므로 필요 없음)

    # 🔹 사용자 이름 출력 시 표현 형식
    def __str__(self):
        # 이메일 → 카카오ID → 네이버ID → 없으면 "Anonymous User"
        return self.email or self.kakao_user_id or self.naver_user_id or "Anonymous User"
