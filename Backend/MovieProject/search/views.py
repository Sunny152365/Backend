import requests  # 외부 API 요청을 위한 라이브러리
from django.shortcuts import render

# OMDb API 키 (본인의 실제 키로 바꿔야 함)
OMDB_API_KEY = '571d7613'  # 이게 진짜 API 키

def search_movie(request):
    """
    영화 제목을 GET 파라미터 'query'로 받아 OMDb API에 검색 요청을 보냄.
    검색 결과(영화 리스트)를 템플릿에 넘겨 렌더링.
    """
    query = request.GET.get('query')  # GET 방식으로 전달된 검색어 받기
    movies = []  # 검색 결과를 담을 리스트 초기화

    if query:  # 검색어가 존재할 때만 API 요청
        # OMDb API 검색 URL 구성 ('s'는 검색어 파라미터)
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}"
        response = requests.get(url)  # API에 GET 요청 전송
        data = response.json()  # 응답 JSON 파싱

        # API가 정상 응답했으면 'Search' 키에 영화 리스트가 있음
        if data.get('Response') == 'True':
            movies = data.get('Search', [])  # 영화 리스트 추출

    # 결과 페이지 렌더링, movies 리스트를 컨텍스트로 전달
    return render(request, 'search/results.html', {'movies': movies})
