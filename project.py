# Making my own Google Assistant through Web Scraping

# 1. 네이버에서 오늘 서울의 날씨 정보를 가져온다
# 2. 헤드라인 뉴스 3건을 가져온다
# 3. IT 뉴스 3건을 가져온다
# 4. 해커스 어학원 홈페이지에서 오늘의 영어 회화 지문을 가져온다

# 미세먼지 00μg/m³ 좋음
# 초미세먼지 00μg/m³ 좋음

# [헤드라인 뉴스]
# 1. 무슨 무슨 일이...
#  (링크)
# 2. 어떤 어떤 일이...
#     ...

from bs4 import BeautifulSoup
import requests
import re

def create_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
    
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def scrape_weather():
    print("[Today's Weather]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    
    weather = soup.find("span", attrs={"class":"weather before_slash"}).get_text()
    since_yesterday = soup.find("span", attrs={"class":"temperature down"}).get_text()
    print("{}, 어제보다 {}".format(weather, since_yesterday))

    curr_temp = soup.find("div", attrs={"class":"temperature_text"}).find("strong").get_text()
    curr_low_temp = soup.find("span", attrs={"class":"temperature_inner"}).find("span", attrs={"class":"lowest"}).get_text()
    curr_high_temp = soup.find("span", attrs={"class":"temperature_inner"}).find("span", attrs={"class":"highest"}).get_text()
    print("{} ({} / {})".format(curr_temp, curr_low_temp, curr_high_temp))

    precipitation = soup.find("div", attrs={"class":"status_wrap"}).find("div", attrs={"class":"temperature_info"})\
        .find("dl", attrs={"class":"summary_list"}).find("dd").get_text()
    humidity = soup.find("div", attrs={"class":"status_wrap"}).find("div", attrs={"class":"temperature_info"})\
        .find("dl", attrs={"class":"summary_list"}).select('dd:nth-child(2 of .desc)')[0].get_text()
    wind = soup.find("div", attrs={"class":"status_wrap"}).find("div", attrs={"class":"temperature_info"})\
        .find("dl", attrs={"class":"summary_list"}).select('dd:nth-child(3 of .desc)')[0].get_text()
    print("강수확률 {} | 습도 {} | 바람 {}".format(precipitation, humidity, wind))
    print()

    dust_info = soup.find("ul", attrs={"class":"today_chart_list"}).find_all("li")[0].a["href"]
    url = "https://search.naver.com/search.naver"+str(dust_info)
    create_soup(url)

    # dust_num = soup.find("li", attrs={"class":"_usaqi _info_layer"}).find("ul").find("li", attrs={"class":"level1 _fine_dust _level"})\
    #     .find("div", attrs={"class":"figure_box _value"}).get_text()
    # print(dust_num)
    # dust_txt = soup.find("li", attrs={"class":"_usaqi _info_layer"}).find("ul").find("li", attrs={"class":"level1 _fine_dust _level"})\
    #     .find("div", attrs={"class":"figure_info"}).find("strong").get_text()

    # fine_dust_num = soup.find("li", attrs={"class":"_usaqi _info_layer"}).find("ul").find("li", attrs={"class":"level1 _ultrafine_dust _level"})\
    #     .find("div", attrs={"class":"figure_box _value"}).get_text()
    # fine_dust_txt = soup.find("li", attrs={"class":"_usaqi _info_layer"}).find("ul").find("li", attrs={"class":"level1 _ultrafine_dust _level"})\
    #     .find("div", attrs={"class":"figure_info"}).find("strong").get_text()
    # print("미세먼지 {} {} | 초미세먼지 {} {}".format(dust_txt, dust_num, fine_dust_txt, fine_dust_num))

def scrape_headline_news():
    print("[Headline News]")
    url = "https://news.naver.com/"
    soup = create_soup(url)

    news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3)
    for idx, news in enumerate(news_list): # Use index so that it prints the index as well
        title = news.a.get_text().strip()
        news_link = url + news.a["href"]
        print("{}. {} \n (Link: {})".format(idx+1, title, news_link))
    print()

def scrape_it_news():
    print("[IT News]")
    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=3)
    for idx, news in enumerate(news_list):
        title = news.select_one("dl dt:nth-of-type(2)").get_text().strip()
        news_link = news.select_one("dl dt:nth-of-type(2)").a["href"]
        print("{}. {} \n (Link: {})".format(idx+1, title, news_link))

def scrape_english():
    print("[Today's English Lesson]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
    soup = create_soup(url)
    
    print("(English)")
    title = soup.find_all("b", attrs={"class":"conv_txtTitle"})
    for korean_title in title[len(title)//2:]:
        print(korean_title.get_text().strip())
    
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    # Half of conv_kor_t are korean, half is english

    for sentence in sentences[len(sentences)//2:]: #8문장이 있다 가정: 5~8 = 영어; starting from length divided by 2
        print(sentence.get_text().strip())
    print()
    
    print("(Korean)")
    for english_title in title[:len(title)//2]:
        print(english_title.get_text().strip())
        
    for sentence in sentences[:len(sentences)//2]: #8문장이 있다 가정: 5~8 = 영어; starting from length divided by 2
        print(sentence.get_text().strip())
    
if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    scrape_headline_news()
    scrape_it_news()
    scrape_english()