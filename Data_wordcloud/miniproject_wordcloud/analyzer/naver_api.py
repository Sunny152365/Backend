import requests
import os
from django.conf import settings

# 네이버 API 정보는 환경변수나 settings.py에 저장
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", getattr(settings, 'NAVER_CLIENT_ID', ''))
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", getattr(settings, 'NAVER_CLIENT_SECRET', ''))

# ✅ 공통 요청 함수
def naver_search(keyword, category):
    if category == 'news':
        url = 'https://openapi.naver.com/v1/search/news.json'
    elif category == 'blog':
        url = 'https://openapi.naver.com/v1/search/blog.json'
    else:
        raise ValueError("지원되지 않는 카테고리입니다.")

    headers = {
        'X-Naver-Client-Id': NAVER_CLIENT_ID,
        'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
    }

    params = {
        'query': keyword,
        'display': 100,  # 최대 100개 가져오기
        'sort': 'date',  # 최신순
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    items = response.json().get('items', [])

    # 뉴스 제목 또는 블로그 제목 + 요약 추출
    titles = [item['title'] + " " + item.get('description', '') for item in items]
    return titles


# ✅ 뉴스 전용 래퍼
def naver_news_search(keyword):
    return naver_search(keyword, 'news')

# ✅ 블로그 전용 래퍼
def naver_blog_search(keyword):
    return naver_search(keyword, 'blog')
