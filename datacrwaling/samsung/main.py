from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
import pandas as pd
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

# 사이드바가 닫혀있으면 열기
sidebar_btn = driver.find_element(By.ID, "wideBtn")
if sidebar_btn.get_attribute('class') == 'btn_wide_off':
    sidebar_btn.click()
    
driver.find_element(By.ID, "4_anchor").click() # <회사 개요> 클릭

# table 데이터 가져오기
tables = utils.get_table_data(driver)