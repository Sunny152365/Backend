import time
import io
import os
from django.shortcuts import render, redirect
from django.http import FileResponse, Http404, HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import date

from .crawler import crawl_news, crawl_blog
from .wordcloud_generator import generate_wordcloud
from .models import SearchHistory, TopKeyword

# 🚧 네이버 API 함수는 따로 구현해야 함 (예시로 import 가정)
from .naver_api import naver_news_search, naver_blog_search  # <- 너가 만들어야 할 함수들


def index(request):
    """
    검색 키워드 입력받는 메인 페이지
    """
    context = {
        'user_authenticated': request.user.is_authenticated
    }
    return render(request, 'analyzer/index.html', context)



def unified_crawl(request):
    """
    검색 결과 처리 뷰 (일반 크롤링 + 네이버 API 통합)
    - 로그인 여부 및 소스에 따라 기능 분기
    - 비회원은 일반 크롤링만 가능하며 하루 3회 제한
    - 요청된 카테고리에 따라 뉴스 또는 블로그 크롤링 실행
    - 워드클라우드 생성 및 DB 저장
    - 결과 템플릿 렌더링
    """
    if request.method != 'POST':
        return redirect('analyzer:index')

    keyword = request.POST.get('keyword')                     # 입력된 키워드
    category = request.POST.get('category', 'news')           # 뉴스 또는 블로그
    source = request.POST.get('source', 'general')            # 일반 또는 네이버 API

    if not keyword:
        return render(request, 'analyzer/index.html', {
            'error': '키워드를 입력하세요.'
        })

    # ✅ 네이버 API는 로그인 사용자만 이용 가능
    if source == 'naver' and not request.user.is_authenticated:
        return HttpResponseForbidden("네이버 API 크롤링은 로그인 사용자만 사용할 수 있습니다.")

    # ✅ 비회원일 경우 일반 크롤링 하루 3회 제한 (세션 기반)
    remaining = None
    if source == 'general' and not request.user.is_authenticated:
        today_key = f'search_count_{date.today()}'
        count = request.session.get(today_key, 0)
        remaining = 3 - count

        if count >= 3:
            return render(request, 'analyzer/limit_exceeded.html', {
                'message': "❌ 비회원은 하루 3회까지만 검색할 수 있습니다.",
                'remaining': 0,
                'count': count
            })

        request.session[today_key] = count + 1
    elif request.user.is_authenticated:
        remaining = None  # 로그인 사용자는 제한 없음

    start = time.time()

    # ✅ 카테고리 및 소스에 따른 크롤링 실행
    if source == 'naver':
        titles = naver_news_search(keyword) if category == 'news' else naver_blog_search(keyword)
    else:
        titles = crawl_news(keyword) if category == 'news' else crawl_blog(keyword)

    elapsed_time = round(time.time() - start, 2)

    # ✅ 검색 결과가 없는 경우 예외 처리
    if not titles:
        return render(request, 'analyzer/result.html', {
            'keyword': keyword,
            'titles': [],
            'time': 0,
            'image_url': None,
            'top_keywords': [],
            'error': "❗ 검색 결과가 없습니다. 키워드를 다시 시도해보세요.",
            'remaining': remaining,
        })

    # ✅ 워드클라우드 이미지 및 상위 키워드 생성
    wc_image, top_keywords = generate_wordcloud(titles, keyword)

    # ✅ 이미지 파일 저장 경로 설정
    filename = f"{source}_wordcloud_{keyword}.png"
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    # ✅ media 폴더 없으면 생성
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    wc_image.save(file_path)

    # ✅ 로그인 사용자일 경우 검색 기록 DB 저장
    if request.user.is_authenticated:
        search_history = SearchHistory.objects.create(
            user=request.user,
            keyword=keyword,
            category=category,
            crawl_duration=elapsed_time
        )

        for word, freq in top_keywords:
            TopKeyword.objects.create(
                search_history=search_history,
                word=word,
                frequency=freq
            )

    # ✅ 결과 페이지로 렌더링
    return render(request, 'analyzer/result.html', {
        'keyword': keyword,
        'titles': titles,
        'time': elapsed_time,
        'image_url': settings.MEDIA_URL + filename,
        'top_keywords': top_keywords,
        'error': None,
        'remaining': remaining,
    })


@login_required
def download_image(request):
    """
    서버 저장 이미지 다운로드
    """
    filename = request.GET.get('filename')

    if not filename:
        raise Http404("파일 이름이 지정되지 않았습니다.")

    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if not os.path.exists(file_path):
        raise Http404("파일이 존재하지 않습니다.")

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)


@login_required
def download_direct(request):
    """
    메모리 내 이미지 직접 다운로드 뷰
    - keyword 쿼리스트링으로 받아 크롤링 후 워드클라우드 생성
    - PIL 이미지 객체를 메모리에서 바로 클라이언트로 전송
    """
    keyword = request.GET.get('keyword')
    category = request.GET.get('category', 'news')  # 기본 news로 설정

    if not keyword:
        return HttpResponse("키워드가 없습니다.", status=400)

    # 실제 크롤링 결과로 titles 얻기
    if category == 'news':
        titles = crawl_news(keyword)
    else:
        titles = crawl_blog(keyword)

    wc_image, _ = generate_wordcloud(titles, keyword)

    # 이미지 객체를 메모리 스트림으로 변환
    img_io = io.BytesIO()
    wc_image.save(img_io, format='PNG')
    img_io.seek(0)

    # HTTP 응답을 파일 다운로드로 설정
    response = HttpResponse(img_io, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename=wordcloud_{keyword}.png'

    return response


@login_required
def history(request):
    """
    로그인한 사용자의 검색 기록 및 상위 키워드 조회
    """
    histories = SearchHistory.objects.filter(user=request.user).order_by('-search_time')

    return render(request, 'analyzer/history.html', {
        'histories': histories
    })
