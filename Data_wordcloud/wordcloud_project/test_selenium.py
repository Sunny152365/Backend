from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 크롬드라이버 경로 (확인한 경로 사용)
chrome_driver_path = "/opt/homebrew/bin/chromedriver"

options = Options()
options.add_argument('--headless')  # 창 안 띄우고 실행
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.naver.com")
print("✅ 네이버 타이틀:", driver.title)

driver.quit()

