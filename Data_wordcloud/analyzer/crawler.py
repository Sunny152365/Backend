# analyzer/crawler.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_driver():
    """
    셀레니움 크롬 드라이버 초기화 (공통 설정)
    """
    options = Options()
    options.add_argument('--headless')  # 브라우저 GUI 없이 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=ko_KR')

    # 네이버 차단 우회를 위한 User-Agent 설정
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    )

    return webdriver.Chrome(options=options)


def crawl_news(keyword):
    """
    ✅ 네이버 뉴스 검색 결과에서 키워드 관련 뉴스 제목 10개 크롤링
    """
    print(f"[크롤링 시작] 뉴스 키워드: {keyword}")
    driver = None

    try:
        driver = get_driver()
        search_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
        driver.get(search_url)

        # 뉴스 타이틀 로딩까지 최대 10초 대기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.news_tit')  # 뉴스 제목 요소
            )
        )

        # 뉴스 제목 요소 모두 수집
        titles = driver.find_elements(By.CSS_SELECTOR, 'a.news_tit')
        print(f"[뉴스 제목 개수] {len(titles)}개 찾음")

        # 최대 10개까지 제목 텍스트 반환
        return [title.text.strip() for title in titles[:10]]

    except Exception as e:
        print(f"❗ 뉴스 크롤링 중 오류 발생: {e}")
        return []

    finally:
        if driver:
            driver.quit()


def crawl_blog(keyword):
    """
    ✅ 네이버 블로그 검색 결과에서 키워드 관련 블로그 제목 10개 크롤링
    """
    print(f"[크롤링 시작] 블로그 키워드: {keyword}")
    driver = None

    try:
        driver = get_driver()
        search_url = f"https://search.naver.com/search.naver?query={keyword}"
        driver.get(search_url)

        # "블로그" 탭이 있으면 클릭 (검색결과에 다른 카테고리가 먼저 나올 수 있음)
        try:
            blog_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "블로그"))
            )
            blog_tab.click()
            print("✅ 블로그 탭 클릭 완료")
            time.sleep(2)  # 탭 전환 후 로딩 대기
        except Exception:
            print("⚠️ 블로그 탭이 없거나 클릭 불가 — 무시하고 진행")

        # 블로그 제목 요소가 로딩될 때까지 최대 15초 대기
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.api_txt_lines.total_tit')  # 블로그 제목
            )
        )

        # 블로그 제목 요소 수집
        # titles = driver.find_elements(By.CSS_SELECTOR, 'a.api_txt_lines.total_tit')  # 기존
        titles = driver.find_elements(By.CSS_SELECTOR, 'a.title_link')  # 변경
        print(f"[블로그 제목 개수] {len(titles)}개 찾음")

        # 크롤링 결과가 없는 경우 메시지 처리
        if len(titles) == 0:
            return ["검색 결과가 없습니다. 더 구체적인 키워드를 입력해주세요."]

        # 최대 10개까지 제목 텍스트 반환
        return [title.text.strip() for title in titles[:10]]

    except Exception as e:
        # 오류 발생 시 현재 페이지를 저장해서 디버깅에 활용
        if driver:
            with open('blog_debug.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("✅ 디버깅용 HTML 저장 완료: blog_debug.html")
        print(f"❗ 블로그 크롤링 중 오류 발생: {e}")
        return ["검색 결과를 불러오는 중 오류가 발생했습니다."]

    finally:
        if driver:
            driver.quit()
