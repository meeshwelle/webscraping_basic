import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml") # 가져온 html문서를 lxml parser를 통해서 BS object로 만듬
# print(soup.title)
# print(soup.title.get_text())
# # print(soup.a) #returns the first found a element in the soup object
# print(soup.a.attrs) # returns in dictionary, of the a element's attribute
# print(soup.a["href"]) # returns the attribute value of href (dictionary!)

# soup.find("a", attrs={"class":"Nbtn_upload"}) #returns the first 'a' element, but with this specific attribute class name
# print(soup.find(attrs={"class":"Nbtn_upload"})) # this also works bc there's only 1 웹툰올리기

# print(soup.find("li", attrs={"class":"rank01"}))
rank1 = soup.find("li", attrs={"class":"rank01"})
# print(rank1.a) # soup을 통해서 발견한 object를 똑같이 return 하기
# print(rank1.a.get_text()) # soup을 통해서 발견한 object를 똑같이 return 하기
# print(rank1.next_sibling) # if returns blank - could be a blank between tags
# print(rank1.next_sibling.next_sibling) # so just do 2 next_sibling!

# rank2 = rank1.next_sibling.next_sibling
# rank3 = rank2.next_sibling.next_sibling
# print(rank3.a.get_text)

# rank2 = rank3.previous_sibling.previous_sibling
# print(rank2.a.get_text())

# print(rank1.parent)

# rank2 = rank1.find_next_sibling("li") # only find the li tags
# print(rank2.a.get_text())
# rank3 = rank2.find_next_sibling("li")
# print(rank3.a.get_text())

# rank2 = rank3.find_previous_sibling("li")
# print(rank2.a.get_text())

# print(rank1.find_next_siblings("li"))

webtoon = soup.find("a", text="연애혁명-379. 이상")
print(webtoon)