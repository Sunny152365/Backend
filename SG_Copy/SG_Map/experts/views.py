from django.views import View
from django.http import JsonResponse
from .models import Expert, Category
from math import radians, cos, sin, asin, sqrt

# 거리 계산 함수 (Haversine 공식)
def haversine(lat1, lon1, lat2, lon2):
    """
    두 좌표(위도, 경도) 간 거리를 km 단위로 계산
    """
    R = 6371  # 지구 반지름(km)
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# 위치 기반 고수 리스트 조회 (카테고리 필터 없음)
class NearbyExpertListView(View):
    def get(self, request):
        """
        요청 쿼리파라미터:
            lat (float): 중심 위도 (필수)
            lng (float): 중심 경도 (필수)
            radius (float): 반경(km), 기본값 5km (선택)
        반환:
            반경 내 고수 리스트 (거리 포함)
        """
        try:
            lat = float(request.GET.get('lat'))
            lng = float(request.GET.get('lng'))
            radius = float(request.GET.get('radius', 5))
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid or missing query parameters'}, status=400)

        experts = Expert.objects.all()
        nearby = []

        for expert in experts:
            distance = haversine(lat, lng, expert.latitude, expert.longitude)
            if distance <= radius:
                nearby.append({
                    'id': expert.id,
                    'name': expert.name,
                    'description': expert.description,
                    'latitude': expert.latitude,
                    'longitude': expert.longitude,
                    'category': expert.category.name,
                    'rating': expert.rating,
                    'review_count': expert.review_count,
                    'hire_count': expert.hire_count,
                    'experience_years': expert.experience_years,
                    'distance_km': round(distance, 2),
                })

        return JsonResponse({'experts': nearby}, json_dumps_params={'ensure_ascii': False})


# 카테고리별 고수 리스트 조회 (ID 또는 이름으로 필터링, 페이징 포함)
class ExpertByCategoryView(View):
    def get(self, request):
        """
        요청 쿼리파라미터:
            category_id (int): 카테고리 ID (우선순위)
            category (str): 카테고리 이름 (category_id 없을 때 사용)
            page (int): 페이지 번호, 기본 1
            page_size (int): 페이지당 아이템 수, 기본 10
        반환:
            해당 카테고리 고수 리스트 및 페이지 정보
        """
        category_id = request.GET.get('category_id')
        category_name = request.GET.get('category')

        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)
        elif category_name:
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)
        else:
            return JsonResponse({'error': 'category_id or category parameter is required'}, status=400)

        experts = category.experts.all()

        # 페이징 처리
        try:
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
        except ValueError:
            return JsonResponse({'error': 'Invalid page or page_size parameter'}, status=400)

        start = (page - 1) * page_size
        end = start + page_size

        experts_page = experts[start:end]

        data = [{
            'id': expert.id,
            'name': expert.name,
            'description': expert.description,
            'latitude': expert.latitude,
            'longitude': expert.longitude,
            'rating': expert.rating,
            'review_count': expert.review_count,
            'hire_count': expert.hire_count,
            'experience_years': expert.experience_years,
        } for expert in experts_page]

        return JsonResponse({
            'category': category.name,
            'page': page,
            'page_size': page_size,
            'total_count': experts.count(),
            'experts': data,
        }, json_dumps_params={'ensure_ascii': False})


# 3단계 추가 — 특정 전문가 리뷰 리스트 조회 API
class ReviewListView(View):
    def get(self, request, expert_id):
        """
        expert_id: URL 파라미터로 받는 전문가 ID
        반환: 해당 전문가의 모든 리뷰 리스트
        """
        try:
            expert = Expert.objects.get(id=expert_id)
        except Expert.DoesNotExist:
            return JsonResponse({'error': 'Expert not found'}, status=404)

        # 역참조 related_name='reviews'를 통해 리뷰 모두 조회
        reviews = expert.reviews.all()
        data = [{
            'reviewer_name': review.reviewer_name,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        } for review in reviews]

        return JsonResponse({
            'expert': expert.name,
            'reviews': data,
        }, json_dumps_params={'ensure_ascii': False})
