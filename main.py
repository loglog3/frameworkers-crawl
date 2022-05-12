from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import boto3
import json
import os
from typing import Optional
from fastapi import FastAPI
from sys import platform
from decouple import config
from fastapi.middleware.cors import CORSMiddleware

INSTAGRAM_ID = config('INSTAGRAM_ID')
INSTAGRAM_PW = config('INSTAGRAM_PW')

def launchDriver():
    chrome_options = Options()
    if platform == 'darwin':
        chrome_options.add_argument('window-size=1920,1080')
        driver = webdriver.Chrome('./chromedriver_mac', chrome_options=chrome_options) # TODO LOCAL
    elif platform == 'linux':
        # TODO LABMDA
        chrome_options.add_argument('--disable-dev-shm-usage') # ??
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x960')
        chrome_options.add_argument('--user-data-dir=/tmp/user-data')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=99')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--data-path=/tmp/data-path')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--homedir=/tmp')
        chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

        # chrome_options.binary_location = '/opt/python/bin/headless-chromium'
        driver = webdriver.Chrome('./chromedriver_linux', chrome_options=chrome_options)
    
    print('크롬 드라이버 생성 됨')
    return driver

def login(driver):
    # driver.get('https://www.instagram.com')
    driver.get('https://www.instagram.com')
    print('인스타 접속 중...')
    sleep(3)
    while True:
        try:
            print('로그인 폼 찾기 시도')
            driver.find_element(by=By.CSS_SELECTOR, value='#loginForm > div > div:nth-child(1) > div > label > input').send_keys(INSTAGRAM_ID) # catdesignshop # gordemafia@gmail.com
            driver.find_element(by=By.CSS_SELECTOR, value=
                '#loginForm > div > div:nth-child(2) > div > label > input').send_keys(INSTAGRAM_PW) # hanseung123! # gorde!@#
            print('로그인 폼 찾기 성공')
            break
        except:
            print('로그인 폼을 찾지 못했습니다')
            driver.get('https://www.instagram.com')
            sleep(10)
    driver.find_element(by=By.CSS_SELECTOR, value=
        '#loginForm > div > div:nth-child(3) > button').click()
    print('로그인 버튼 클릭...')
    sleep(10) # 로그인 대기


def get_users_by_crawling(driver, instagram_id):
    """instagram_id 고객의 팔로잉 명단 리스트를 반환합니다. 또는 오류 발생시 False 를 반환합니다
    """
    driver.get(f'https://www.instagram.com/{instagram_id}')
    print(f'이동 중... https://www.instagram.com/{instagram_id}')
    sleep(2) # 검색할 계정 페이지 이동 대기

    user_instagram_feed_check_count = 0
    while True:
        try:
            팔로잉버튼 = driver.find_element(
                by=By.CSS_SELECTOR, value='section > main > div > header > section > ul > li:nth-child(3) > a > div')
            break
        except:
            sleep(2)
            print('실패, 재시도합니다')
            user_instagram_feed_check_count += 1
            if user_instagram_feed_check_count == 5:
                print('최종 실패했습니다')
                return False
    
    팔로잉수 = 팔로잉버튼.get_attribute('textContent')
    팔로잉버튼.click()
    sleep(2)

    print('팔로잉 목록 받아오기 시작...')
    loop_index = 0
    loop_buffer = 0
    loop_breaker = False
    while True:
        height = driver.execute_script(
            "return document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollHeight")
        driver.execute_script(
            f"document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollTo(0, {height})")
        while True: # 무한스크롤로 새로운 스크롤을 받아오면 바로 넘어감
            new_height = driver.execute_script(
                "return document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollHeight")
            if height == new_height:
                loop_buffer += 1
                if (loop_buffer == 8):
                    loop_breaker = True
                    break
                sleep(0.5)
                continue
            else:
                break
        loop_buffer = 0
        loop_index += 1
        if loop_breaker == True:
            break

    print('팔로잉 목록 받아오기 종료...')
    def getNames(element):
        text_content = element.get_attribute('textContent')
        text_content = text_content.replace('Follow', '')
        text_content = text_content.replace('Following', '')
        text_content = text_content.replace('팔로잉', '')
        text_content = text_content.replace('팔로우', '')
        text_content = text_content.replace('인증됨', '')
        text_content = text_content.replace('Verified', '')
        print('😡', text_content)
        return text_content
        return {userId: textContent.split(' ')[0], userName: textContent.split(' ')[1]}

    elements = driver.find_elements(by=By.CSS_SELECTOR, value="body > div.RnEpo.Yx5HN > div > div > div > div.isgrP > ul > div > li")
    names = list(map(getNames, elements))

    print('총 루프 수', loop_index)
    print('크롤링수', len(names), '팔로잉수', 팔로잉수)
    return names


app = FastAPI()
possibility = True
# driver = launchDriver()
# login(driver)

origins = [
    "*",
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
    "http://frameworkers.net",
    "https://frameworkers.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    print('heach check 성공!')
    return {"Hello": "I'm here"}

@app.get("/possibility")
def read_root():
    global possibility
    print('지금 가능한지 여부 확인하기')
    return {"Hello": possibility}


@app.get("/instagram")
def read_item(user_id: str):
    global possibility
    if possibility == False:
        print("이미 실행중인 크롤링이 있습니다")
        return {"지금"}
    possibility = False
    names = get_users_by_crawling(driver, user_id)
    possibility = True
    if names == False:
        return {"result": "실패"}
    else:
        return names

@app.on_event("shutdown")
def shutdown_event():
    print('FAST API가 종료됩니다')
    # global driver
    # driver.quit()
    # print('chromium 을 종료했습니다')