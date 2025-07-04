# analyzer/crawler.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def get_driver():
    """
    셀레니움 크롬 드라이버 초기화 (공통)
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=ko_KR')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    )
    return webdriver.Chrome(options=options)

def crawl_news(keyword):
    """
    네이버 뉴스에서 키워드 관련 제목을 10개 크롤링
    """
    print(f"[크롤링 시작] 뉴스 키워드: {keyword}")
    driver = None
    try:
        driver = get_driver()
        driver.get(f"https://search.naver.com/search.naver?where=news&query={keyword}")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.sds-comps-text-type-headline1'))
        )

        titles = driver.find_elements(By.CSS_SELECTOR, 'span.sds-comps-text-type-headline1')
        print(f"[뉴스 제목 개수] {len(titles)}개 찾음")
        return [title.text.strip() for title in titles[:10]]

    except Exception as e:
        print(f"❗ 뉴스 크롤링 중 오류 발생: {e}")
        return []

    finally:
        if driver:
            driver.quit()

def crawl_blog(keyword):
    """
    네이버 블로그에서 키워드 관련 제목을 10개 크롤링
    """
    print(f"[크롤링 시작] 블로그 키워드: {keyword}")
    driver = None

    try:
        driver = get_driver()
        search_url = f"https://search.naver.com/search.naver?query={keyword}"
        driver.get(search_url)

        # 블로그 탭 존재 시 클릭
        try:
            blog_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "블로그"))
            )
            blog_tab.click()
            print("✅ 블로그 탭 클릭 완료")
            time.sleep(2)  # 렌더링 대기
        except Exception:
            print("⚠️ 블로그 탭이 없거나 클릭 불가 — 무시하고 계속 진행")

        # 블로그 제목 로딩
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.api_txt_lines.total_tit')
            )
        )

        titles = driver.find_elements(By.CSS_SELECTOR, 'a.api_txt_lines.total_tit')
        print(f"[블로그 제목 개수] {len(titles)}개 찾음")

        if not titles:
            return ["검색 결과가 없습니다. 더 구체적인 키워드를 입력해주세요."]

        return [title.text.strip() for title in titles[:10]]

    except Exception as e:
        if driver:
            with open('blog_debug.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("✅ 디버깅용 HTML 저장 완료: blog_debug.html")
        print(f"❗ 블로그 크롤링 중 오류 발생: {e}")
        return ["검색 결과를 불러오는 중 오류가 발생했습니다."]

    finally:
        if driver:
            driver.quit()
