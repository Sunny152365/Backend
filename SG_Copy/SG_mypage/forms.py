from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()  # AUTH_USER_MODEL에 지정된 User 모델 자동 사용

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'profile_image', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
