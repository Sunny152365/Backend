from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models

# 사용자 생성 및 관리하는 매니저 클래스
class UserManager(BaseUserManager):
    # 일반 사용자 생성 메서드 (email or social id 반드시 필요)
    def create_user(self, email=None, password=None, **extra_fields):
        if not email and not extra_fields.get("kakao_user_id") and not extra_fields.get("naver_user_id"):
            raise ValueError("The user must have either email or a social ID.")
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, **extra_fields)

        # 비밀번호가 있으면 해싱 처리, 없으면 비밀번호 사용 불가 상태로 설정
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    # 슈퍼유저 생성 메서드 (email, password 필수)
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)      # 관리자 권한 부여
        extra_fields.setdefault("is_superuser", True)  # 최고 관리자 권한 부여
        extra_fields.setdefault("is_active", True)     # 활성화 상태

        if not email:
            raise ValueError("Superuser must have an email address")
        if not password:
            raise ValueError("Superuser must have a password")

        return self.create_user(email=email, password=password, **extra_fields)

    # 역할별 사용자 생성 메서드: 의뢰인
    def create_client(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'client')
        return self.create_user(email, password, **extra_fields)

    # 역할별 사용자 생성 메서드: 고수
    def create_pro(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_type', 'pro')
        return self.create_user(email, password, **extra_fields)


# 사용자 모델 정의 (커스텀 유저 모델)
class User(AbstractBaseUser, PermissionsMixin):
    # 사용자 이름 (실명 또는 닉네임)
    name = models.CharField(max_length=150, null=True, blank=True)
    
    # 이메일 (기본 로그인 수단, 선택적)
    email = models.EmailField(unique=True, null=True, blank=True)
    
    # 소셜 로그인 ID (카카오, 네이버)
    kakao_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    naver_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    # 사용자 상태
    is_active = models.BooleanField(default=True)   # 계정 활성화 여부
    is_staff = models.BooleanField(default=False)   # 관리자 페이지 접근 가능 여부

    # Django 기본 그룹 및 권한 필드
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

    # 역할 구분 필드 (의뢰인 client, 고수 pro)
    USER_TYPE_CHOICES = (
        ('client', '의뢰인'),
        ('pro', '고수'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')

    # 프로필 이미지 (선택 사항)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # 연락처 (선택 사항)
    phone_number = models.CharField(max_length=20, blank=True)

    # 자기소개 (선택 사항)
    bio = models.TextField(blank=True)

    # 가입일자 및 최종 로그인 (관리 및 분석용)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # 소셜 로그인 여부 (optional, 편리 확인용)
    is_kakao = models.BooleanField(default=False)
    is_naver = models.BooleanField(default=False)

    # 매니저 객체 등록 (기본 유저 생성 메서드 포함)
    objects = UserManager()

    # 로그인 필드 지정 (이메일)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # createsuperuser 명령 시 필수 필드 (email은 USERNAME_FIELD에 포함)

    def __str__(self):
        # 출력 시 이메일, 카카오ID, 네이버ID, 없으면 Anonymous User 반환
        return self.email or self.kakao_user_id or self.naver_user_id or "Anonymous User"
