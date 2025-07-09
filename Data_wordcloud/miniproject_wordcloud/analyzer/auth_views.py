from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
import re

# 회원가입 폼 클래스: 아이디와 비밀번호에 대한 유효성 검사 포함
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)  # 아이디 필드만 사용

    # 아이디 형식 검사: 4~20자, 영문+숫자만 허용
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9]{4,20}$', username):
            raise forms.ValidationError("아이디는 4~20자의 영문자와 숫자만 사용할 수 있습니다.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 사용 중인 아이디입니다.")
        return username

    # 비밀번호 일치 및 형식 검사
def clean_password2(self):
    # 입력된 비밀번호 두 개를 가져옴
    pw1 = self.cleaned_data.get('password1')
    pw2 = self.cleaned_data.get('password2')

    # ✅ 비어 있는 경우 예외 처리 (안전성 보강)
    if not pw1 or not pw2:
        raise forms.ValidationError("비밀번호와 비밀번호 확인을 모두 입력해주세요.")

    # 두 비밀번호가 일치하는지 확인
    if pw1 != pw2:
        raise forms.ValidationError("비밀번호가 일치하지 않습니다.")

    # 비밀번호 길이 검사
    if len(pw1) < 8:
        raise forms.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")

    # 대문자 포함 여부
    if not re.search(r'[A-Z]', pw1):
        raise forms.ValidationError("비밀번호에 대문자가 하나 이상 포함되어야 합니다.")

    # 소문자 포함 여부
    if not re.search(r'[a-z]', pw1):
        raise forms.ValidationError("비밀번호에 소문자가 하나 이상 포함되어야 합니다.")

    # 숫자 포함 여부
    if not re.search(r'[0-9]', pw1):
        raise forms.ValidationError("비밀번호에 숫자가 하나 이상 포함되어야 합니다.")

    # 특수문자 포함 여부
    if not re.search(r'[\W_]', pw1):
        raise forms.ValidationError("비밀번호에 특수문자가 하나 이상 포함되어야 합니다.")

    return pw2


    # 저장 시 비밀번호 암호화 처리
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # 비밀번호 해시 저장
        if commit:
            user.save()
        return user

# 회원가입 뷰 함수
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # 폼에 POST 데이터 바인딩
        if form.is_valid():
            user = form.save()  # 사용자 생성
            login(request, user)  # 가입 후 바로 로그인 처리
            return redirect('index')  # 메인 페이지로 이동
    else:
        form = CustomUserCreationForm()  # 빈 폼 생성
    return render(request, 'analyzer/signup.html', {'form': form})

# 로그인 뷰 함수
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # 장고 기본 로그인 폼 사용
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # 로그인 처리
            return redirect('analyzer:index')
    else:
        form = AuthenticationForm()
    return render(request, 'analyzer/login.html', {'form': form})

# 로그아웃 뷰 함수
def logout_view(request):
    # 로그아웃 처리 코드
    logout(request)  # 세션 삭제

    # 네임스페이스를 포함해서 리다이렉트
    return redirect('analyzer:index')