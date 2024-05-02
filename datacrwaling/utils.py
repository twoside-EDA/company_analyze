from bs4 import BeautifulSoup 
import pandas as pd
from selenium.webdriver.common.by import By

def get_table_data(driver):
    result = []
    
    # Detail page 활성화
    iframe = driver.find_element(By.ID, 'ifrm')
    driver.switch_to.frame(iframe)

    # Detail page html 가져오기
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 테이블 태그 요소 모두 찾기
    tables = soup.find_all('table')
    results = []  
    
    # 테이블의 각 행과 열에서 데이터 추출
    for table in tables:
        temp_data = []
        data = []

        # 테이블 행 별로 추출 (텍스트, rowspan, colspan) 
        for row in table.find_all('tr'):
            temp_row_data = []
            row_data = []
            
            for cell in row.find_all(['th', 'td']):
                rowspan, colspan = 1, 1
                if 'rowspan' in cell.attrs:
                    rowspan = int(cell.attrs['rowspan'])
                if 'colspan' in cell.attrs:
                    colspan = int(cell.attrs['colspan'])

                ## 수치형 데이터면 숫자로 변경
                item = cell.get_text(strip=True)
                item = int(item) if item.isdigit() else item

                for _ in range(colspan):
                    temp_row_data.append((item, rowspan))
                    row_data.append(item)

            temp_data.append(temp_row_data)
            data.append(row_data)

        # table 태그를 이용해서 적었지만 table이 아닌 것들
        if len(data) < 2: 
            continue
            
        # rowspan 데이터 추가하기
        for row_idx, row in enumerate(temp_data):
            for col_idx, cell in enumerate(row):
                item, rowspan = cell
                
                if rowspan > 1:
                    for i in range(1, rowspan):
                        data[row_idx + i].insert(col_idx, item)
        try:
            df = pd.DataFrame(data[1:], columns=data[0])        
            results.append(df)
            
        except Exception as e:
            df = pd.DataFrame(data[2:], columns=data[1])
            results.append(df)
        
    # Detail page 비활성화
    driver.switch_to.default_content()
    
    return results
    