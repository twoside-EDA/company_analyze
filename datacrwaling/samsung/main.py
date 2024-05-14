from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

import sys
import os
# 부모 폴더의 경로를 가져옵니다.
parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)
import utils

# 삼성전자 2023.12 사업보고서 열기
url = 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=20240312000736'
driver = webdriver.Chrome()
driver.get(url)

## 사이드 바 버튼 가져오기
sidebar_btn = driver.find_element(By.ID, "wideBtn")

cnt = 0
wanted_pages = [4, 5, 9, 11, 12, 13, 15, 16, ] ## 크롤링 원하는 페이지 ## 왠지 모르겠는데 101페이지 py파일에서 크롤링이 안됨...

for i in wanted_pages:
    # side bar 안 열려 있으면 열기
    if sidebar_btn.get_attribute('class') == 'btn_wide_off':
        sidebar_btn.click()

    ## 페이지 이동
    try:
        page = driver.find_element(By.ID, f"{i}_anchor")
        page_title = page.text
        print(page_title)

        page.click()
    except NoSuchElementException:
        continue
        
    time.sleep(3)

    ## 테이블 가져오기
    tables = utils.get_table_data(driver)
    print(f"cur page : {i}\t table count : {len(tables)}")
    cnt += len(tables)
    
    ## 테이블 csv로 변환
    for idx, table in enumerate(tables):
        table.to_csv(f'data/{page_title}({idx+1}).csv', index=False)

    print("success crawling")
    
    
print(cnt)