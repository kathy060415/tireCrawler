from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# CHROMEDRIVER_PATH = './crawler/drivers/chromedriver' # Windows는 chromedriver.exe로 변경
CHROMEDRIVER_PATH = 'C:\Program Files (x86)\chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument( "--headless" )     # 크롬창이 열리지 않음
chrome_options.add_argument( "--no-sandbox" )   # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_options.add_argument( "--disable-gpu" )  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_options.add_argument(f"--window-size={ WINDOW_SIZE }")
chrome_options.add_argument('Content-Type=application/json; charset=utf-8')

driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options )
driver.get('https://www.tirerack.com/content/tirerack/desktop/en/tires/by-brand.html')