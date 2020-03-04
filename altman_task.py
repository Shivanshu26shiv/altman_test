
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

options.add_argument("--headless")
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\Xarvis-PC\Desktop\chromedriver_win32\chromedriver.exe')


def parse_team(url):
    
    driver.get(url)
    for a in driver.find_elements_by_xpath('.//a'):
        link = a.get_attribute('href')
        team_url = link.split(url)[-1]
        print('1:', team_url)
        team_url = re.sub('\W+',' ', team_url)
        print('2:', team_url)
        for _ in team_strings:
            if team_url.count(_):
                print('team_link:', link)
                link_list.append(link)
                return

try:
    team_strings = ['team', 'people']
    link_list = []        
    # url='https://www.cinven.com/'
    url=['www.kkr.com', 'http://www.cinven.com', 'www.kkr.com', 'www.american-securities.com', 'www.hf.com', 'www.bcpartners.com']
    for _ in url:
        parse_team(url)
        
    print('link_list:', link_list)

finally:
    print('Execution done!')
    driver.quit()

