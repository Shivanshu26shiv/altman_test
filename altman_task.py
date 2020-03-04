
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

            if sublink_flag == 2:
                flag = 0
                for _ in [name_list, position_list]:
                    for __ in _:
                        try:
                            element = driver.find_element_by_class_name(__).text
                            print('element:', element)
                            flag = 1
                            break
                        except:
                            # print(__, 'class not found', url)
                            continue
                        '''    
                        if flag == 0:
                            print('new:', 'http://'+url+sub_link)
                            # parse_equity_urls('http://'+url+sub_link, 2)
                        '''
                for _ in [bio_list]:
                    for __ in _:
                        if __ == 'markdown':
                            try:
                                elements = driver.find_elements_by_class_name(__)
                                for ___ in elements:
                                    print('markdowns:', ___.text)
                            except:
                                print(__, 'class not found', url)
                                continue
                        else:
                            try:
                                element = driver.find_element_by_class_name(__).text
                                print('element:', element)
                                flag = 1
                                break
                            except:
                                # print(__, 'class not found', url)
                                continue

                        
            for a in driver.find_elements_by_xpath('.//a'):
                link = a.get_attribute('href')
                link = link.split('://')[-1]
                link = link.rstrip('/')
                if link[:3] != 'www':
                    link = 'www.'+link
                
                hash_char_absent = link.split('/')[-1].count('#')
                if hash_char_absent:
                    if sublink_flag == 2:
                        link = link.rstrip('#')
                        # print('link-hash_char_absent_0:', link, hash_char_absent)
                    else:
                        # print('link-hash_char_absent_1:', link, hash_char_absent)
                        continue

                try:
                    sub_link = ''
                    temp = list(set(link.split(url)))
                    if len(temp) > 1:
                        sub_link = temp[-1]
                        # print('sub_link:', sub_link)
                    else:
                        print('link_0:', link)
                        continue
                except AttributeError:
                    continue

                print('sub_link:', sub_link)
                if sub_link in ['/extended-network']:
                    continue
                
                if sublink_flag == 0:
                    
                    parsed_sub_link = re.sub('\W+',' ', sub_link, flags=re.IGNORECASE)

                    print('parsed_sub_link:', parsed_sub_link)

                    for _ in team_strings:
                        if parsed_sub_link.count(_):
                            print('team_link:', link)
                            parse_equity_urls('http://'+link, 1)                        
                            break
                        
                elif sublink_flag == 1:
                    print('link-url:', link, url)
                    
                    if len(list(set(link.split(url)))) > 1:
                        print('link:', link)
                        parse_equity_urls('http://'+link, 2)


            # if not returned before then return 0
            return 0

        finally:
            driver.quit()

try:
    team_strings = ['team', 'people']
    name_list = ['name', 'person-name', 'bio-right']
    position_list = ['position', 'person-title', 'bio-right']
    bio_list = ['bio', 'markdown', 'content-right-wide']
    team_dict={}

    '''
    url_list=['http://www.cinven.com']
    
    # url_list=['http://www.cinven.com', 'http://www.kkr.com', 'http://www.american-securities.com', 'http://www.hf.com', 'http://www.bcpartners.com']

    for url in url_list:
        returned_link = parse_equity_urls(url)
        team_dict[url] = returned_link
        
    print('team_dict:', team_dict)
    '''

    parse_equity_urls('http://www.hf.com', 0)

finally:
    print('\nExecution done!')

