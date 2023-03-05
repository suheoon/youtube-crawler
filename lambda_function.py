import json
import time
import string
import requests, zipfile, io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_driver():
    # chrome driver option 설정
    try:
        options = Options()
        options.binary_location = '/opt/headless-chromium'
        options.add_argument('lang=en')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1500,1000")
        options.add_argument(
            'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        driver = webdriver.Chrome('/opt/chromedriver', chrome_options=options)
        return driver
        
    except Exception as e:
        return e

def lambda_handler(event, context):
    # 최신 노래방 곡 정보 다운로드
    r = requests.get('https://d26jfubr2fa7sp.cloudfront.net/Musics.zip')
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("/tmp")
    
    # 기존 youtube_Url 다운로드
    
    # TJ 노래방 곡 정보 파싱
    tj_dic = {}
    f = open("/tmp/musicbook_TJ.txt", "rt")
    while True:
        line = f.readline()
        if line == '' :
            break
        s = line.split(sep='^')
        if s :
            keyword = s[0] + " " + s[1]
            number = s[2]
            tj_dic[number] = keyword
    f.close()
    
    # URL 정보 파싱
    url_number_list = []
    f = open("/tmp/youtube_Url.txt", "rt")
    while True:
        line = f.readline()
        if line == '':
            break
        s = line.split(sep='^')
        if s:
            number = s[0]
            url_number_list.append(number)
    f.close()
    
    # URL에 반영되지 않은 최신 노래 정보 저장
    new_info = []
    for number, title in tj_dic.items():
        if number not in url_number_list:
            new_info.append(number+"^"+title)
    
    # f = open("/tmp/youtube_Url.txt", "rt")
    
    for info in new_info:
        search = info.split(sep='^')
        if not search:
            continue
        number = search[0]
        keyword = search[1]
        
        # driver 설정
        driver = get_driver()
        for character in string.punctuation:
            keyword = keyword.replace(character, ' ')
        # 검색 키워드 설정: 키워드 내 띄어쓰기는 URL에서 '+'로 표시되기 때문에 이에 맞게 변환
        SEARCH_KEYWORD = keyword.replace(' ', '+')
        if (SEARCH_KEYWORD == '\n'):
            break
        # # 스크래핑 할 URL 세팅
        URL = "https://www.youtube.com/results?search_query=" + SEARCH_KEYWORD
        # # 크롬 드라이버를 통해 지정한 URL의 웹 페이지 오픈
        driver.get(URL)
        time.sleep(3)
        # # 페이지 소스 추출
        html_source = driver.page_source
        soup_source = BeautifulSoup(html_source, 'html.parser')
        
        # driver.close()
        driver.quit()
        
        # # 모든 콘텐츠 정보
        content_total = soup_source.find_all(class_ = 'yt-simple-endpoint style-scope ytd-video-renderer')
        # # 콘텐츠 링크만 추출
        content_total_link = list(map(lambda data: "https://youtube.com" + data["href"], content_total))
        url = str(content_total_link[0]).replace('https://youtube.com/watch?v=','')
        print("테스트",url)
        # f.write(number + '^' + url + '^' + '\n')
    
    response = {
        "statusCode": 200,
        "body": json.dumps("업데이트 성공")
    }

    return response