import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/list?titleId=675554"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
cartoons = soup.find_all("td", attrs={"class":"title"}) # in list form
title = cartoons[0].a.get_text()
link = cartoons[0].a["href"]
print(title)
print("https://comic.naver.com"+link)

# 만화 제목 + 링크
for cartoon in cartoons:
    title = cartoon.a.get_text()
    link = "https://comic.naver.com"+cartoon.a["href"]
    print(title, link)

# 평점 구하기    
cartoons = soup.find_all("div", attrs={"class" : "rating_type"})
rates = 0
for cartoon in cartoons:
    rate = cartoon.find("strong").get_text() # element 'strong' tag
    print(rate)
    rates += float(rate)
print("Total rate: ", rates)
    
avg = rates / len(cartoons)
print("Average rate: ",avg)
