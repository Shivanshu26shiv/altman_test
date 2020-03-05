
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import time
 

options = Options()

options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

chrome_driver_path = r'C:\Users\Xarvis-PC\Desktop\chromedriver_win32\chromedriver.exe'

driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)

try:
    URL = "https://www.american-securities.com/en/team/helen-chiang"
    driver.get(URL)
    e = driver.find_elements_by_css_selector("div.markdown > p")
    for _ in e:
        print(_.text)

finally:
    driver.quit()
