# analyzer/views.py

import io
import base64
import traceback
from django.shortcuts import render
from . import crawler
from wordcloud import WordCloud


def home(request):
    """홈 화면: 키워드 입력 폼만 출력"""
    return render(request, "analyzer/home.html")


def result(request):
    """검색 → 크롤링 → 워드클라우드 생성 → 이미지 반환"""
    if request.method != "POST":
        return render(request, "analyzer/home.html")

    try:
        keyword = request.POST.get("keyword")
        category = request.POST.get("category")

        print("POST 받은 키워드:", keyword)
        print("POST 받은 카테고리:", category)

        if category == "news":
            texts = crawler.crawl_news(keyword)
        elif category == "blog":
            texts = crawler.crawl_blog(keyword)
        else:
            texts = []

        if not texts or all("검색 결과가 없습니다" in text for text in texts):
            return render(
                request,
                "analyzer/home.html",
                {"error": "❗ 결과를 찾을 수 없습니다. 다른 키워드로 시도해보세요."},
            )

        full_text = " ".join(texts)

        font_path = (
            "/System/Library/Fonts/Supplemental/AppleGothic.ttf"  # macOS용 한글 폰트
        )
        wc = WordCloud(
            font_path=font_path, width=800, height=400, background_color="white"
        ).generate(full_text)

        buffer = io.BytesIO()
        wc.to_image().save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return render(
            request,
            "analyzer/result.html",
            {"wordcloud_img": img_base64, "keyword": keyword},
        )

    except Exception as e:
        print("❌ 예외 발생:", e)
        traceback.print_exc()
        return render(request, "analyzer/home.html", {"error": f"오류 발생: {str(e)}"})
