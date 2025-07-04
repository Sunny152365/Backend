from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_driver():
    """
    셀레니움 크롬 드라이버 초기화 (공통)
    """
    options = Options()
    options.add_argument('--headless')  # GUI 없이 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=ko_KR')
    # 💡 네이버 접근 차단 우회용 User-Agent
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
        search_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
        driver.get(search_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'span.sds-comps-text-type-headline1')
            )
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
    네이버 블로그에서 키워드 관련 제목 10개 크롤링 + 핵심 HTML 일부 저장
    """
    print(f"[크롤링 시작] 블로그 키워드: {keyword}")
    driver = None

    try:
        driver = get_driver()
        search_url = f"https://search.naver.com/search.naver?query={keyword}"
        driver.get(search_url)

        # 📌 "블로그" 탭 클릭 시도 (쇼핑, 음악 우선 노출 방지용)
        try:
            blog_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "블로그"))
            )
            blog_tab.click()
            print("✅ 블로그 탭 클릭 완료")
            time.sleep(2)  # 렌더링 여유
        except Exception as e:
            print(f"⚠️ 블로그 탭 클릭 실패, 무시하고 진행: {e}")

        # ✅ 변경된 셀렉터: 블로그 제목 a 태그 class = 'title_link'
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a.title_link')  # 🔥 핵심 변경
            )
        )

        titles = driver.find_elements(By.CSS_SELECTOR, 'a.title_link')  # 🔥 핵심 변경
        print(f"[블로그 제목 개수] {len(titles)}개 찾음")

        # 💡 제목 HTML 일부 저장 (디버깅용)
        with open('blog_debug_partial.html', 'w', encoding='utf-8') as f:
            for title in titles[:5]:
                f.write(title.get_attribute('outerHTML') + '\n\n')
        print("✅ 주요 블로그 제목 일부 HTML 저장 완료: blog_debug_partial.html")

        if len(titles) == 0:
            return ["검색 결과가 없습니다. 더 구체적인 키워드를 입력해주세요."]

        return [title.text.strip() for title in titles[:10]]

    except Exception as e:
        if driver:
            with open('blog_debug.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print("✅ 전체 페이지 HTML 저장 완료: blog_debug.html")
        print(f"❗ 블로그 크롤링 중 오류 발생: {e}")
        return ["검색 결과를 불러오는 중 오류가 발생했습니다."]

    finally:
        if driver:
            driver.quit()
