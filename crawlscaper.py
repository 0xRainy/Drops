import time
import os
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


def grab_data_longest_winning_streaks():
    """Returns list of players Top Winning Sreaks from
       http://crawl.akrasiac.org/scoring/streaks.html"""

    url = "http://crawl.akrasiac.org/scoring/streaks.html"
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.quit()
    table = soup.findChildren('tr')
    user_list = ['test', 'test2']
    for child in table:
        child = child.findNext('a')
        child = str(child)
        user = child.split('>')[1]
        user = user.split('<')[0]
        user = user.lower()
        if user in user_list:
            pass
        elif len(user_list) < 20:
            user_list.append(user)
        else:
            pass
    return user_list


# Output super long userlist to txt file for checking results of #
# grab_data_longest_winning_streaks()                            #
##################################################################
# with open('TopStreakPlayers.txt', 'w') as f:
#     for i in grab_data_longest_winning_streaks():
#         f.write(i + '\n')


def grabdata_all_crawl_sites():
    """Returns dict of players and site they are using"""

    url = "https://crawl.develz.org/watch.htm"
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.quit()
    table = soup.findChildren('tr')
    user_dict = {'test': 'testsite', 'test2': 'testsite2'}
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


TOP_PLAYERS = grab_data_longest_winning_streaks()
ACTIVE_PLAYERS = grabdata_all_crawl_sites()

FOUND_PLAYERS = []
for top_player in TOP_PLAYERS:
    if top_player in ACTIVE_PLAYERS:
        FOUND_PLAYERS.append(top_player)
if not FOUND_PLAYERS:
    print('No Top Players Found')
else:
    for i in FOUND_PLAYERS:
        print(i, ACTIVE_PLAYERS[i])
