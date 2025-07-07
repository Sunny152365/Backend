# analyzer/wordcloud_generator.py

from wordcloud import WordCloud
from collections import Counter
from PIL import Image
import numpy as np
import os
from pathlib import Path

def generate_wordcloud(texts, keyword):
    """
    texts: 크롤링된 제목 리스트
    keyword: 검색 키워드 (파일명 등에 사용)
    
    반환: PIL Image 객체, 상위 키워드 리스트 [(단어, 빈도), ...]
    """
    # 텍스트 리스트를 하나의 문자열로 병합
    text = ' '.join(texts)

    # macOS에서 한글 폰트 경로 지정 (시스템 내장 폰트)
    font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
    
    # 만약 해당 경로에 폰트가 없으면 프로젝트 내 fonts 폴더에 폰트가 있다고 가정하고 상대 경로 설정 가능
    # base_dir = Path(__file__).resolve().parent
    # font_path = os.path.join(base_dir, 'fonts', 'NanumGothic.ttf')

    # 워드클라우드 생성 (한글 폰트 필수, 그래야 한글 글자가 깨지지 않음)
    wc = WordCloud(
        font_path=font_path,      # macOS 시스템 폰트 경로
        background_color='white', # 배경 흰색
        width=800,               # 가로 크기
        height=600               # 세로 크기
    )
    wc.generate(text)            # 텍스트 기반 워드클라우드 생성

    # 워드클라우드에서 추출된 단어 빈도 정보
    counter = Counter(wc.words_)
    top_keywords = counter.most_common(3)  # 상위 3개 키워드 추출

    # 생성된 워드클라우드를 PIL 이미지 객체로 변환
    image = wc.to_image()

    return image, top_keywords
