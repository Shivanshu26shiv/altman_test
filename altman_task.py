
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        WebDriverException,
                                        ElementClickInterceptedException,
                                        ElementNotInteractableException)
import csv
from bs4 import BeautifulSoup


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

def parse_equity_urls(url):

    global lst
    
    try:
        driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
    except:
        try:
            driver.quit()
            driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
        except:
            driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
            
    driver.get(url)

    try:
        url = url.split('://')[-1]
        url = url.rstrip('/')

        print('1:', url)
        team_link_flag = 0

        for a in driver.find_elements_by_xpath('.//a'):
            link = a.get_attribute('href')
            try:
                link = link.split('://')[-1]
            except AttributeError:
                continue
            link = link.rstrip('/')
            if link[:3] != 'www':
                link = 'www.'+link

            try:
                temp = list(set(link.split(url)))
                if len(temp) > 1:
                    sub_link = temp[-1]
                    # print('sub_link:', sub_link)
                    if sub_link.count('#'):
                        continue
                else:
                    # print('link_0:', link)
                    continue
            except AttributeError:
                continue

            if sub_link in ['/extended-network']:
                continue

            # team link search
            parsed_sub_link = re.sub('\W+',' ', sub_link, flags=re.IGNORECASE)

            for _ in team_strings:
                if parsed_sub_link.count(_):
                    if url not in team_link_dict.keys():
                        if url == 'www.kkr.com':
                            link = 'www.kkr.com/our-firm/leadership'
                        team_link_dict[url] = link
                        print('nest_1:', link)
                        team_link_flag = 1
                        break

            if team_link_flag == 1:
                break

        if team_link_flag == 0:
            print('No team link found!')
        else:
            try:
                driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
            except:
                try:
                    driver.quit()
                    driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
                except:
                    driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)

            driver.get('http://'+link)
            print('final_l:', link)

            ## kkr ############
            if link == 'www.kkr.com/our-firm/leadership':

                kkr_html = driver.find_element_by_tag_name("html").get_attribute('outerHTML')
                kkr_html = kkr_html.replace('<!--', '')
                kkr_html = kkr_html.replace('-->', '')

                link_lst = []
                soup = BeautifulSoup(kkr_html, features="lxml")
                for link in soup.findAll('a', attrs={'href': re.compile("^https://www.kkr.com/our-firm/leadership")}):
                    link_lst.append(link.get('href'))
                link_lst = list(set(link_lst))

                print('l:', len(link_lst))

                for link_1 in link_lst:
                    if link_1.count('?'):
                        continue
                    try:
                        link_1 = link_1.split('://')[-1]
                    except AttributeError:
                        continue
                    link_1 = link_1.rstrip('/')
                    if link_1[:3] != 'www':
                        link_1 = 'www.' + link_1
                    if link_1 == link:
                        continue

                    print('new_link:', link_1)

                    ########################
                    myurl = link_1.partition('/')[0]
                    d = {}
                    d[myurl] = {}
                    d[myurl]['Profile'] = link_1
                    d[myurl]['URL'] = link

                    try:
                        driver = webdriver.Chrome(options=options,
                                                  executable_path=chrome_driver_path)
                    except:
                        try:
                            driver.quit()
                            driver = webdriver.Chrome(options=options,
                                                      executable_path=chrome_driver_path)
                        except:
                            driver = webdriver.Chrome(options=options,
                                                      executable_path=chrome_driver_path)

                    driver.get('http://' + link_1)

                    for _ in [name_list]:
                        d[myurl]['Name'] = ''
                        for __ in _:
                            try:
                                element = driver.find_element_by_class_name(__).text
                                # print('element:', element)
                                d[myurl]['Name'] = element
                                break
                            except:
                                # print(__, 'class not found', url)
                                pass
                    for _ in [position_list]:
                        d[myurl]['Position'] = ''
                        for __ in _:
                            try:
                                # print('__', __)
                                element = driver.find_element_by_class_name(__).text
                                if element == d[myurl]['Name']:
                                    d[myurl]['Name'] = element.splitlines()[0]
                                    d[myurl]['Position'] = element.splitlines()[1]
                                else:
                                    d[myurl]['Position'] = element
                                break
                            except:
                                # print(__, 'class not found', link)
                                pass
                    print('bio_list:', bio_list)
                    for _ in [bio_list]:
                        d[myurl]['Bio'] = ''
                        for __ in _:
                            print('__', __)

                            try:
                                element = driver.find_element_by_class_name(__)
                                d[myurl]['Bio'] = element.text
                                break
                            except NoSuchElementException:
                                continue

                                '''
                                try:
                                    element = driver.find_element_by_class_name(__).text
                                    # print('element:', element)
                                    d[myurl]['Bio'] = element
                                    print('>>>', __, d[myurl]['Bio'])

                                    if len(d[myurl]['Name']) == 0 and len(d[myurl]['Position']) == 0 and \
                                                    len(d[myurl]['Bio']) != 0:
                                        d[myurl]['Name'] = d[myurl]['Bio'].splitlines()[0]
                                        d[myurl]['Position'] = d[myurl]['Bio'].splitlines()[1]
                                        d[myurl]['Bio'] = d[myurl]['Bio'].splitlines()[2:]

                                except:
                                    print(__, 'class not found', url)
                                '''

                    lst.append(d[myurl])
                    if len(lst) == 2 :
                        return lst


                    #########################

                ## kkr ############

            else:

                contains = link.split('/')[-1]
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                for b in driver.find_elements_by_xpath("//a[contains(@href, '" + contains + "')]"):
                    link_1 = b.get_attribute('href')
                    if link_1.count('?'):
                        continue
                    try:
                        link_1 = link_1.split('://')[-1]
                    except AttributeError:
                        continue
                    link_1 = link_1.rstrip('/')
                    if link_1[:3] != 'www':
                        link_1 = 'www.' + link_1
                    if link_1 == link:
                        continue

                    print('new_link_1:', link_1)

                    ########################
                    myurl = link_1.partition('/')[0]
                    d = {}
                    d[myurl] = {}
                    d[myurl]['Profile'] = link_1
                    d[myurl]['URL'] = link

                    try:
                        driver = webdriver.Chrome(options=options,
                                                  executable_path=chrome_driver_path)
                    except:
                        try:
                            driver.quit()
                            driver = webdriver.Chrome(options=options,
                                                      executable_path=chrome_driver_path)
                        except:
                            driver = webdriver.Chrome(options=options,
                                                      executable_path=chrome_driver_path)

                    driver.get('http://' + link_1)

                    for _ in [name_list]:
                        d[myurl]['Name'] = ''
                        for __ in _:
                            try:
                                element = driver.find_element_by_class_name(__).text
                                # print('element:', element)
                                d[myurl]['Name'] = element
                                break
                            except:
                                # print(__, 'class not found', url)
                                pass
                    for _ in [position_list]:
                        d[myurl]['Position'] = ''
                        for __ in _:
                            try:
                                # print('__', __)
                                element = driver.find_element_by_class_name(__).text
                                if element == d[myurl]['Name']:
                                    d[myurl]['Name'] = element.splitlines()[0]
                                    d[myurl]['Position'] = element.splitlines()[1]
                                else:
                                    d[myurl]['Position'] = element
                                break
                            except:
                                # print(__, 'class not found', link)
                                pass
                    # print('bio_list:', bio_list)
                    for _ in [bio_list]:
                        d[myurl]['Bio'] = ''
                        for __ in _:
                            # print('__', __)

                            if __ == 'markdown':
                                e = driver.find_elements_by_css_selector("div.markdown > p")
                                for _ in e:
                                    d[myurl]['Bio'] += _.text
                                break

                            try:
                                element = driver.find_element_by_class_name(__)
                                d[myurl]['Bio'] = element.text
                                if len(d[myurl]['Name']) == 0 and len(d[myurl]['Position']) == 0:
                                    d[myurl]['Name'] = d[myurl]['Bio'].splitlines()[0]
                                    d[myurl]['Position'] = d[myurl]['Bio'].splitlines()[1]
                                    d[myurl]['Bio'] = d[myurl]['Bio'].splitlines()[2:]
                                break
                            except NoSuchElementException:
                                continue

                    lst.append(d[myurl])
                    if len(lst) == 2 :
                        return lst

                        #########################

    finally:
        driver.quit()

try:
    lst = []
    team_link_dict = {}
    team_strings = ['team', 'people']
    name_list = ['name', 'person-name', 'bio-right']
    position_list = ['position', 'person-title', 'bio-right', 'desc']
    bio_list = ['bio', 'markdown', 'content-right-wide', 'featured-team-member+p']

    # url_list=['http://www.cinven.com', 'http://www.american-securities.com', 'http://www.hf.com', 'http://www.bcpartners.com',
    # 'http://www.kkr.com']
    url_list = ['http://www.cinven.com']

    for url in url_list:
        lst = parse_equity_urls(url)
    
    # parse_equity_urls('http://www.kkr.com/our-firm/leadership', 1)

finally:
    try:
        driver.quit()
    except:
        pass

    csv_columns = ['URL', 'Profile', 'Name', 'Position', 'Bio']
    with open("scrapped_output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerow({'URL': '', 'Profile': '', 'Name': '', 'Position': '', 'Bio': ''})
        for data in lst:
            writer.writerow(data)

    print(team_link_dict)
    print('\nExecution done!')
    

