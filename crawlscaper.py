import time
from selenium import webdriver
from bs4 import BeautifulSoup

url = "http://crawl.akrasiac.org:8080/#lobby"
browser = webdriver.PhantomJS()
browser.get(url)
time.sleep(0.05)  # Change this to some sort of 'Wait for response'
soup = BeautifulSoup(browser.page_source, "lxml")
browser.quit()
table = soup.findAll('td', {"class": "username"})
a = []
for x in table:
    x.find_all('a')
    for y in x:
        y = str(y)
        y = y.split('>')[1]
        y = y.split('<')[0]
        a.append(''.join(y))
[print(i) for i in a]
