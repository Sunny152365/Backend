import time
import io
import os
from django.shortcuts import render
from django.http import FileResponse, Http404, HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import date

from .crawler import crawl_news, crawl_blog
from .wordcloud_generator import generate_wordcloud
from .models import SearchHistory, TopKeyword


def index(request):
    """
    검색 키워드 입력받는 메인 페이지
    """
    context = {
        'user_authenticated': request.user.is_authenticated
    }
    return render(request, 'analyzer/index.html', context)



def result(request):
    """
    검색 결과 처리 뷰 (로그인 유무에 따라 기능 분기)
    """
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        category = request.POST.get('category')

        # ✅ 비회원 3회 제한 처리 (세션 기반)
        if not request.user.is_authenticated:
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

        start = time.time()

        # ✅ 카테고리에 따른 크롤링 실행
        if category == 'news':
            titles = crawl_news(keyword)
        else:
            titles = crawl_blog(keyword)

        elapsed_time = round(time.time() - start, 2)

        # ✅ 워드클라우드 생성
        wc_image, top_keywords = generate_wordcloud(titles, keyword)

        filename = f"wordcloud_{keyword}.png"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # media 폴더가 없으면 생성
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        wc_image.save(file_path)

        # ✅ 로그인 사용자일 경우에만 DB 기록
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

        # ✅ 템플릿으로 결과 전달
        if not titles:
            return render(request, 'analyzer/result.html', {
                'keyword': keyword,
                'titles': [],
                'time': 0,
                'image_url': None,
                'top_keywords': [],
                'error': "❗ 검색 결과가 없습니다. 키워드를 다시 시도해보세요."
            })

        return render(request, 'analyzer/result.html', {
            'keyword': keyword,
            'titles': titles,
            'time': elapsed_time,
            'image_url': settings.MEDIA_URL + filename,
            'top_keywords': top_keywords,
            'error': None,
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
