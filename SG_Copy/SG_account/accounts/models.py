from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email and not extra_fields.get("kakao_user_id") and not extra_fields.get("naver_user_id"):
            raise ValueError("The user must have either email or a social ID.")
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError("Superuser must have an email address")
        if not password:
            raise ValueError("Superuser must have a password")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    kakao_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    naver_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

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

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        # 이메일 있으면 이메일, 없으면 카카오아이디 또는 네이버아이디 리턴
        return self.email or self.kakao_user_id or self.naver_user_id or "Anonymous User"


