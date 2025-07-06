# analyzer/wordcloud_generator.py

from wordcloud import WordCloud
from collections import Counter
from PIL import Image
import numpy as np

def generate_wordcloud(texts, keyword):
    """
    texts: 크롤링된 제목 리스트
    keyword: 검색 키워드 (파일명 등에 사용)
    
    반환: PIL Image 객체, 상위 키워드 리스트 [(단어, 빈도), ...]
    """
    # 텍스트 병합
    text = ' '.join(texts)

    # 워드클라우드 생성
    wc = WordCloud(font_path='NanumGothic.ttf', background_color='white', width=800, height=600)
    wc.generate(text)

    # 상위 키워드 추출
    counter = Counter(wc.words_)
    top_keywords = counter.most_common(3)

    # PIL Image 객체 반환
    image = wc.to_image()

    return image, top_keywords
