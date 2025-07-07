from pathlib import Path
import os

# manage.py가 위치한 폴더를 기준으로 프로젝트 최상위 경로 지정
BASE_DIR = Path(__file__).resolve().parent.parent

# Django 보안용 비밀 키 (개발 중일 땐 노출 주의)
SECRET_KEY = "django-insecure-)aip(6_f!te#7gn(@jo%pt-td8d1_*ic_iz#gx3(a$_&@t=kij"

# 개발 모드 여부 (실서비스시 False로 변경 필수)
DEBUG = True

ALLOWED_HOSTS = []

# 설치된 앱 목록 (기본 + analyzer 앱 포함)
INSTALLED_APPS = [
    "django.contrib.admin",           # 관리자 사이트
    "django.contrib.auth",            # 인증 시스템
    "django.contrib.contenttypes",    
    "django.contrib.sessions",        
    "django.contrib.messages",        
    "django.contrib.staticfiles",     # 정적파일 처리

    "analyzer",                       # 사용자 정의 앱
]

# 미들웨어 설정 (요청 처리 과정 중간에 작동)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL 설정 모듈
ROOT_URLCONF = "miniproject_wordcloud.urls"

# 템플릿 설정
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 템플릿을 찾는 경로 지정:
        # analyzer 앱 내부 templates 폴더를 명시적으로 포함
        "DIRS": [os.path.join(BASE_DIR, "analyzer", "templates", 'analyzer')],
        # 각 앱의 templates 폴더 자동 탐색 허용
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",    # 템플릿에서 request 객체 사용 가능
                "django.contrib.auth.context_processors.auth",   # 인증 관련 템플릿 변수 제공
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI 애플리케이션 경로
WSGI_APPLICATION = "miniproject_wordcloud.wsgi.application"

# 데이터베이스 설정 (기본 SQLite 사용)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # DB파일 위치
    }
}

# 비밀번호 유효성 검사기 설정
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 국제화 및 시간대 설정
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 정적파일 접근 URL (브라우저에서 접근하는 경로)
STATIC_URL = "/static/"

# 정적 파일 위치: analyzer 앱 내부 static 폴더 지정
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "analyzer", "static", 'analyzer'),
]

# 미디어 파일(사용자 업로드 파일) URL 및 저장 위치 설정
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 기본 자동 필드 타입 설정
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
