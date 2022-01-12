from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://naver.com")
elem = browser.find_element_by_class_name('link_login').click()

browser.find_element_by_id('id').clear()
browser.find_element_by_id('id').send_keys("my_id")

# html 정보 출력
print(browser.page_source)