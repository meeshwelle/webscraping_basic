import requests
from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")

browser = webdriver.Chrome(options=options)

url = "https://play.google.com/store/movies/collection/cluster?clp=0g4XChUKD3RvcHNlbGxpbmdfcGFpZBAHGAQ%3D:S:ANO1ljJvXQM&gsr=ChrSDhcKFQoPdG9wc2VsbGluZ19wYWlkEAcYBA%3D%3D:S:ANO1ljK7jAA"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
browser.get(url)

import time
interval = 2 # seconds

# save current height of browser
prev_height = browser.execute_script("return document.body.scrollHeight")

# 반복 수행
while True:
    # Scroll to bottom of the page
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    # Wait for page to load
    time.sleep(interval)
    
    # Save current height of the page again, but now variable is different!
    curr_height = browser.execute_script("return document.body.scrollHeight")
    if curr_height == prev_height:
        break
    
    prev_height = curr_height
    
print("Scroll Complete")
browser.get_screenshot_as_file("google_movie.png")

res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

movies = soup.find_all("div", attrs={"class":"ImZGtf mpg5gc"})
print(len(movies))

for movie in movies:
    title = movie.find("div", attrs={"class":"WsMG1c nnK0zc"}).get_text()
    
    # 할인 전 가격
    original_price = movie.find("span", attrs={"class":"SUZt4c djCuy"})
    if original_price:
        original_price = original_price.get_text()
    else:
        # print(title, "할인 되지 않은 영화 제외")
        continue
    
    # 할인 된 가격
    price = movie.find("span", attrs={"class":"VfPpfd ZdBevf i5DZme"}).get_text()
    
    # 링크 정보
    link = movie.find("a", attrs={"class":"JC71ub"})["href"]
    print(f"Title: {title}")
    print(f"Price before sale: {original_price}")
    print(f"Price after sale: {price}")
    print("Links: ", "https://play.google.com"+link)
    print("-"*100)
    
# browser.quit()