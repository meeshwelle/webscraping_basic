import csv
from os import symlink
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

url = "https://swingtradebot.com/equities?page="
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}

filename = "listOfStocks.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "Symbol 	Grade	Name	Close	Volatility	Avg Volume".split("\t")
writer.writerow(title)

for page in range(1, 6):
    res = requests.get(url+str(page), headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    
    # Find all elements of 한 줄 of the table
    data_rows = soup.find("table", attrs={"class":"table table-striped table-bordered"}).find("tbody").find_all("tr") # in list form

    # For each element of 한 줄
    for idx, row in enumerate(data_rows):
        # 각 각 상자들
        columns = row.find_all("td")
        
        print("============= Stock {}_{} =============".format(page, idx+1))
        print("Symbol: ", columns[0].get_text().strip())
        print("Grade: ", columns[2].get_text().strip())
        print("Name: ", columns[3].get_text().strip())
        print("Close: ", columns[4].get_text().strip())
        print("Volatility: ", columns[5].get_text().strip())
        print("Avg Volume: ", columns[6].get_text().strip())
        
        # data = [column.get_text().strip() for column in columns] # data = tag td가 가지고 있는 정보들
        # print(data)
        # the commented lines are same as the below codes:
        list_data = []
        for idx, column in enumerate(columns):
            if len(column.get_text()) == 0:
                continue
            data = column.get_text().strip()
            list_data.append(data)
        print(list_data)