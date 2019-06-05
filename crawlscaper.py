import time
from selenium import webdriver
from bs4 import BeautifulSoup


# This works for each individual site #

# url = "http://crawl.berotato.org:8080/#lobby"
# browser = webdriver.PhantomJS()
# browser.get(url)
# time.sleep(2)  # Change this to some sort of 'Wait for response'
# soup = BeautifulSoup(browser.page_source, "lxml")
# browser.quit()
# table = soup.findAll('td', {"class": "username"})
# a = []
# for x in table:
#     x.find_all('a')
#     for y in x:
#         y = str(y)
#         y = y.split('>')[1]
#         y = y.split('<')[0]
#         a.append(''.join(y))
# [print(i) for i in a]

# This grabs from a list of every active player on all crawl sites
def GrabData_AllCrawlSites():
    url = "https://crawl.develz.org/watch.htm"
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.quit()
    table = soup.findChildren('tr')
    user_dict = {}
    for child in table:
        child = child.findNext('a')
        child = str(child)
        site = child.split('//')[-1]
        site = site.split('/')[0]
        if site == 'crawl.project357.org':
            user = child.split('h/')[1]
        else:
            user = child.split('-')[-1]
        user = user.split('"')[0]
        # user_dict.update({user: site})
        user_dict[user] = site
    return user_dict


print(GrabData_AllCrawlSites())
