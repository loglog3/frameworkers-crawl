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
        chrome_options.add_argument('--window-size=1280x1696')
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

    return driver

def login(driver):
    driver.get('https://www.instagram.com')
    print('인스타 접속 중...')
    sleep(2)
    driver.find_element(by=By.CSS_SELECTOR, value='#loginForm > div > div:nth-child(1) > div > label > input').send_keys(INSTAGRAM_ID) # catdesignshop # gordemafia@gmail.com
    driver.find_element(by=By.CSS_SELECTOR, value=
        '#loginForm > div > div:nth-child(2) > div > label > input').send_keys(INSTAGRAM_PW) # hanseung123! # gorde!@#
    driver.find_element(by=By.CSS_SELECTOR, value=
        '#loginForm > div > div:nth-child(3) > button').click()
    print('로그인 버튼 클릭...')
    sleep(3) # 로그인 대기

def get_users_by_crawling(driver, instagramId):
    driver.get(f'https://www.instagram.com/{instagramId}')
    print(f'이동 중... https://www.instagram.com/{instagramId}')
    sleep(10) # 검색할 계정 페이지 이동 대기

    팔로잉버튼 = driver.find_element(by=By.CSS_SELECTOR, value=
        '#react-root > section > main > div > header > section > ul > li:nth-child(3) > a > div')
    팔로잉수 = 팔로잉버튼.get_attribute('textContent')
    팔로잉버튼.click()
    sleep(3)

    print('팔로잉 목록 받아오기 시작...')
    loop_index = 0
    while True:
        height = driver.execute_script(
            "return document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollHeight")
        driver.execute_script(
            f"document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollTo(0, {height})")
        if loop_index < 5:
            sleep(0.8)
        elif loop_index < 10:
            sleep(1.2)
        elif loop_index < 20:
            sleep(1.5)
        elif loop_index < 30:
            sleep(1.7)
        else:
            sleep(2)

        new_height = driver.execute_script(
            "return document.querySelector('body > div.RnEpo.Yx5HN > div > div > div > div.isgrP').scrollHeight")
        if height == new_height:
            break
        loop_index += 1

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
driver = launchDriver()
login(driver)

@app.get("/possibility")
def read_root():
    global possibility
    print('지금 가능한지 여부 확인하기')
    return {"Hello": possibility}


@app.get("/")
def read_item(user_id: str):
    global possibility
    if possibility == False:
        print("이미 실행중인 크롤링이 있습니다")
        return {"지금"}
    possibility = False
    names = get_users_by_crawling(driver, user_id)
    possibility = True
    return names

