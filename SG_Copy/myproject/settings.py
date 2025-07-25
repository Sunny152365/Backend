"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 4.2.21.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from django.http import HttpResponseRedirect
import pymysql
pymysql.install_as_MySQLdb()

HttpResponseRedirect.allowed_schemes = [
    'http',
    'https',
    'ftp',
    'mailto',
    'naverkhs0sahddsysi5rd5brf',  # 커스텀 스킴 반드시 소문자 유지하세요
]

from pathlib import Path

class PrintRequestPathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        print(f"Requested URL path: {request.path}")
        response = self.get_response(request)
        return response

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# AUTH_USER_MODEL = 'SG_account.accounts.User'
AUTH_USER_MODEL = 'accounts.User'  # app_label.ModelName 형태

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tvr+%e+#)okx#_q4ok!furn&*p7n4rg6-#p*_qm(bq=_&p^yp+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 테스트용 모든 호스트 허용
ALLOWED_HOSTS = ['*']
# 일반적으로 허용할 때
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '172.30.1.91']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'SG_account.accounts',
    'django_extensions',
    'SG_mypage',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS는 가장 위에 위치 권장
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',       # MySQL 사용
        'NAME': 'mydb',                             # MySQL 데이터베이스 이름
        'USER': 'woniluser',                        # MySQL 사용자명
        'PASSWORD': 'strongpassword123',           # MySQL 비밀번호
        'HOST': 'localhost',                        # MySQL 서버 주소 (로컬이면 localhost)
        'PORT': '3306',                             # MySQL 포트 (기본 3306)
        'OPTIONS': {
            'charset': 'utf8mb4',                   # 문자셋 설정 (한글 등 지원용)
            'use_unicode': True,                     # 유니코드 사용 여부
        },
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
from decouple import config

NAVER_CLIENT_ID = config('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = config('NAVER_CLIENT_SECRET')
NAVER_REDIRECT_URI = config('NAVER_REDIRECT_URI')

KAKAO_REST_API_KEY = config('KAKAO_REST_API_KEY')
KAKAO_CLIENT_SECRET = config('KAKAO_CLIENT_SECRET')
KAKAO_REDIRECT_URI = config('KAKAO_REDIRECT_URI')

INSTALLED_APPS += ['corsheaders']
# MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + MIDDLEWARE

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://4fca-182-224-45-138.ngrok-free.app",  # ngrok 프론트 주소
    'http://localhost:3000',  # 프론트 URL에 맞게 조정
    ]
# settings.py

SESSION_COOKIE_SECURE = False  # 개발 시 반드시 False
SESSION_COOKIE_SAMESITE = 'Lax'  # or 'None' (if using cross-origin, 'None' + Secure)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 기본값, 없어도 됨

CSRF_COOKIE_SECURE = False

# settings.py

CORS_ALLOW_CREDENTIALS = True
# settings.py
SESSION_COOKIE_SAMESITE = "None"  # 웹뷰/외부 도메인 이동 시 필수
SESSION_COOKIE_SECURE = True      # HTTPS에서만 세션 쿠키를 전송 (ngrok이 https여야 함)

# 또는 실제 배포 주소
NAVER_REDIRECT_URI = 'https://4fca-182-224-45-138.ngrok-free.app/api/naver/callback/'
# NAVER_REDIRECT_URI = 'naver_3lM5JlNiGaw3TTgWDa3://auth'

from django.utils.http import url_has_allowed_host_and_scheme

# 허용할 스킴 리스트
ALLOWED_REDIRECT_SCHEMES = ['http', 'https', 'ftp', 'mailto', 'naverkhs0sahddsysi5rd5brf']

# settings.py
NAVER_CALLBACK_SCHEME = 'naverKhS0SAhDdsySi5rd5bRf'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
