import requests
import logging
from urllib.parse import urlencode

from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, serializers
from rest_framework.decorators import api_view

from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View


User = get_user_model()
logger = logging.getLogger(__name__)

def redirect_custom_scheme(url):
    response = HttpResponse(status=302)
    response['Location'] = url
    return response

# ----------------------- Email Login -----------------------
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class EmailLoginView(APIView):
    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)
        return Response(serializer.errors, status=400)


# ----------------------- Kakao Login -----------------------
class KakaoLoginView(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token required'}, status=400)

        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
            response.raise_for_status()
        except requests.RequestException:
            return Response({'success': False, 'error': 'Failed to get Kakao profile'}, status=500)

        profile = response.json()
        kakao_user_id = profile.get('id')
        email = profile.get('kakao_account', {}).get('email')

        if not kakao_user_id:
            return Response({'success': False, 'error': 'Kakao user ID not found'}, status=401)

        user = User.objects.filter(kakao_user_id=kakao_user_id).first()
        if not user:
            user = User.objects.create(kakao_user_id=kakao_user_id, email=email or "")
        elif email and not user.email:
            user.email = email
            user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {'email': user.email},
        })


# ----------------------- Naver Login -----------------------
class NaverLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({'error': 'Access token required'}, status=400)

        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
            response.raise_for_status()
        except requests.RequestException:
            return Response({'error': 'Failed to fetch Naver profile'}, status=500)

        data = response.json()
        if data.get('resultcode') != '00':
            return Response({'error': 'Invalid Naver token data'}, status=401)

        user_info = data.get('response', {})
        naver_user_id = user_info.get('id')
        email = user_info.get('email')

        if not naver_user_id:
            return Response({'error': 'Naver user ID not found'}, status=401)

        user = User.objects.filter(naver_user_id=naver_user_id).first()
        if not user:
            user = User.objects.create(naver_user_id=naver_user_id, email=email or "")
        elif email and not user.email:
            user.email = email
            user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'email': user.email,
                'nickname': getattr(user, 'nickname', None),
            }
        })


# ----------------------- Naver Callback -----------------------
class NaverCallbackView(APIView):
    def get(self, request):
        logger.info(f"Request query params: {request.query_params}")
        return self.handle_callback(request.query_params)

    def post(self, request):
        return self.handle_callback(request.data)

    def handle_callback(self, params):
        code = params.get("code")
        state = params.get("state")

        logger.info(f"[NAVER CALLBACK] code={code}, state={state}")

        if not code or not state:
            return Response({"error": "code or state missing"}, status=status.HTTP_400_BAD_REQUEST)

        token_data = self.get_token_from_naver(code, state)
        if "error" in token_data:
            return self.redirect_error("naver_token_error", token_data)

        access_token = token_data.get("access_token")
        if not access_token:
            return self.redirect_error("access_token_missing", token_data)

        profile_data = self.get_profile_from_naver(access_token)
        if profile_data.get("resultcode") != "00":
            return self.redirect_error("profile_error", profile_data)

        try:
            user = self.get_or_create_user(profile_data["response"])
            refresh = RefreshToken.for_user(user)

            query = urlencode({
                "token": str(refresh.access_token),
                "refresh": str(refresh),
                "id": user.id,
                "email": user.email,
                "name": user.name,
            })

            # 별도 success 경로로 리디렉션 (쿼리 포함)
            redirect_url = f"https://4fca-182-224-45-138.ngrok-free.app/api/naver/callback/success/?{query}"
            return redirect(redirect_url)

        except Exception as e:
            logger.exception("[NAVER USER PROCESSING ERROR]")
            return self.redirect_error("server_error", {"message": str(e)})

    def redirect_error(self, error_code, detail=None):
        query = urlencode({
            "error": error_code,
            "detail": str(detail) if detail else ""
        })
        redirect_url = f"https://4fca-182-224-45-138.ngrok-free.app/api/naver/callback/error/?{query}"
        return redirect(redirect_url)

    def get_token_from_naver(self, code, state):
        token_url = "https://nid.naver.com/oauth2.0/token"
        params = {
            "grant_type": "authorization_code",
            "client_id": settings.NAVER_CLIENT_ID,
            "client_secret": settings.NAVER_CLIENT_SECRET,
            "code": code,
            "state": state,
        }
        try:
            response = requests.get(token_url, params=params, timeout=5)
            response.raise_for_status()
            token_data = response.json()
            logger.info(f"[NAVER TOKEN] {token_data}")
            return token_data
        except requests.RequestException as e:
            logger.error(f"[NAVER TOKEN ERROR] {str(e)}")
            return {"error": "네이버 토큰 요청 실패", "message": str(e)}

    def get_profile_from_naver(self, access_token):
        profile_url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get(profile_url, headers=headers, timeout=5)
            response.raise_for_status()
            profile_data = response.json()
            logger.info(f"[NAVER PROFILE] {profile_data}")
            return profile_data
        except requests.RequestException as e:
            logger.error(f"[NAVER PROFILE ERROR] {str(e)}")
            return {"resultcode": "99", "message": "네이버 프로필 요청 실패", "error": str(e)}

    def get_or_create_user(self, user_info):
        naver_id = user_info["id"]
        email = user_info.get("email") or f"{naver_id}@naver.com"
        name = user_info.get("name") or "네이버 사용자"

        user = User.objects.filter(naver_user_id=naver_id).first()
        if user:
            return user

        user = User.objects.filter(email=email).first()
        if user:
            user.naver_user_id = naver_id
            if not user.name or not user.name.strip():
                user.name = name
            user.save()
            return user

        return User.objects.create(
            naver_user_id=naver_id,
            email=email,
            name=name,
        )


@method_decorator(csrf_exempt, name='dispatch')
class NaverCallbackSuccessView(View):
    def get(self, request):
        token = request.GET.get("token")
        refresh = request.GET.get("refresh")
        user_id = request.GET.get("id")
        email = request.GET.get("email")
        name = request.GET.get("name")

        # 앱의 커스텀 URL 스킴으로 리디렉션
        if token and refresh and user_id:
            app_redirect_url = f"naverKhS0SAhDdsySi5rd5bRf://login?token={token}&refresh={refresh}&id={user_id}&email={email}&name={name}"
            return redirect(app_redirect_url)

        return HttpResponse("로그인 성공, 하지만 전달 정보가 부족합니다.", status=400)


@method_decorator(csrf_exempt, name='dispatch')
class NaverCallbackErrorView(View):
    def get(self, request):
        error = request.GET.get("error")
        detail = request.GET.get("detail", "")
        return HttpResponse(f"Error: {error}, Detail: {detail}", status=400)

# ----------------------- Register -----------------------
@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')

    if not email or not password:
        return Response({"error": "Email and password are required."}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists."}, status=400)

    user = User.objects.create(
        email=email,
        password=make_password(password),
        name=name,
    )

    return Response({"message": "User registered successfully."}, status=201)
