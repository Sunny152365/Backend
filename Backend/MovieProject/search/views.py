import requests
import re
from django.shortcuts import render
from decouple import config  # python-decouple로 .env 읽기

# 🔑 .env에서 API 키 읽기
TMDB_API_KEY = config('TMDB_API_KEY')
OMDB_API_KEY = config('OMDB_API_KEY')

def is_korean(text):
    """
    검색어에 한글이 포함되어 있는지 확인
    """
    return bool(re.search(r'[가-힣]', text))

def search_tmdb(query):
    """
    TMDb API로 영화 검색
    """
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'ko-KR',
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    if data.get('results'):
        for m in data['results']:
            results.append({
                'title': m.get('title', ''),
                'year': m.get('release_date', '')[:4] if m.get('release_date') else '정보없음',
                'poster': f"https://image.tmdb.org/t/p/w200{m['poster_path']}" if m.get('poster_path') else '',
            })
    return results

def search_omdb(query):
    """
    OMDb API로 영화 검색 (영어 중심)
    """
    url = "http://www.omdbapi.com/"
    params = {
        'apikey': OMDB_API_KEY,
        's': query,
        'type': 'movie',
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    if data.get('Response') == 'True':
        for m in data.get('Search', []):
            results.append({
                'title': m.get('Title', ''),
                'year': m.get('Year', ''),
                'poster': m.get('Poster') if m.get('Poster') != 'N/A' else '',
            })
    return results

def search_movie(request):
    """
    사용자의 검색어가 한글이면 TMDb로, 영어면 OMDb로 요청
    """
    query = request.GET.get('query')
    movies = []

    if query:
        if is_korean(query):
            movies = search_tmdb(query)
        else:
            movies = search_omdb(query)

    return render(request, 'search/results.html', {'movies': movies})
