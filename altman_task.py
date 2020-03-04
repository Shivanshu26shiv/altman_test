
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


def parse_equity_urls(url, sublink_flag=0):


    driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\Xarvis-PC\Desktop\chromedriver_win32\chromedriver.exe')
    driver.get(url)
    
    url = url.split('://')[-1]
    url = url.rstrip('/')

    print('sublink_flag-url:', sublink_flag, url)

    hash_char_absent = url.split('/')[-1].count('#')
    if not hash_char_absent:
        # print('url-hash_char_absent:', url, hash_char_absent)
        try:
            
            for a in driver.find_elements_by_xpath('.//a'):
                link = a.get_attribute('href')
                link = link.split('://')[-1]
                link = link.rstrip('/')
                
                hash_char_absent = link.split('/')[-1].count('#')
                if hash_char_absent:
                    if sublink_flag == 2:
                        link = link.rstrip('#')
                        # print('link-hash_char_absent_0:', link, hash_char_absent)
                    else:
                        # print('link-hash_char_absent_1:', link, hash_char_absent)
                        continue

                try:
                    if len(list(set(link.split(url)))) > 1:
                        sub_link = list(set(link.split(url)))[-1]
                        # print('sub_link:', sub_link)
                    else:
                        continue
                except AttributeError:
                    continue

                print('sub_link:', sub_link)
                
                if sublink_flag == 0:
                    
                    parsed_sub_link = re.sub('\W+',' ', sub_link, flags=re.IGNORECASE)

                    print('parsed_sub_link:', parsed_sub_link)

                    for _ in team_strings:
                        if parsed_sub_link.count(_):
                            print('team_link:', link)
                            parse_equity_urls(link, 1)                        
                            break
                        
                elif sublink_flag == 1:
                    print('link-url:', link, url)
                    
                    if len(list(set(link.split(url)))) > 1:
                        print('link:', link)
                        parse_equity_urls('http://'+link, 2)

                elif sublink_flag == 2:

                    for _ in [name_list, position_list, bio_list]:
                        for __ in _:
                            try:
                                element = driver.find_element_by_class_name(__).text
                                print('element:', element)
                                break
                            except:
                                print(__, 'class not found')
                                continue

            # if not returned before then return 0
            return 0

        finally:
            driver.quit()

try:
    team_strings = ['team', 'people']
    name_list = ['name']
    position_list = ['position']
    bio_list = ['bio']
    team_dict={}

    '''
    url_list=['http://www.cinven.com']
    
    # url_list=['http://www.cinven.com', 'http://www.kkr.com', 'http://www.american-securities.com', 'http://www.hf.com', 'http://www.bcpartners.com']

    for url in url_list:
        returned_link = parse_equity_urls(url)
        team_dict[url] = returned_link
        
    print('team_dict:', team_dict)
    '''

    parse_equity_urls('https://www.cinven.com', 0)

finally:
    print('\nExecution done!')

