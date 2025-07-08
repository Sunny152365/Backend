from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

# 커스텀 UserChangeForm
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')

# 커스텀 UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

# 실제 Admin 클래스 정의
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    ordering = ['email']
    list_display = ['email', 'is_staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    search_fields = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
