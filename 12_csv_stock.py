import csv
import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="

filename = "시가총액1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE	토론실".split("\t")
writer.writerow(title)

for page in range(1, 5): # upto 4 pages
    res = requests.get(url+str(page))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    
    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    # print(data_rows)
    
    for row in data_rows:
        columns = row.find_all("td")
        # print(columns)
        if len(columns) <= 1: #의미없는 data는 skip
            continue
        data = [column.get_text().strip() for column in columns] # data = tag td가 가지고 있는 정보들
        print(data)
        # writer.writerow(data) #return in list