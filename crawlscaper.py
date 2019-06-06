""" This script functions as a sort of 'Twitch.tv' for DCSS online servers
    allowing the user to be notified when a top 20, on one or more
    selected leaderboard,is active and playing.
    It provides a link to spectate these players.
"""
import time
from pathlib import Path
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


class Leaderboards():
    """Handles choosing a leaderboard to download data from.
       The filename parameter must include *.txt
    """
    def __init__(self, leaderboard_type='', filename=''):
        self.leaderboard_type = leaderboard_type
        self.filename = filename

    def grab_leaderboard_data(self):
        """Downloads leaderbord data from leaderboard_type (url) and outputs
           formatted list to file separated by newline."""
        filename = self.filename
        url = self.leaderboard_type
        browser = webdriver.PhantomJS()
        browser.get(url)
        soup = None
        while soup is None:
            soup = BeautifulSoup(browser.page_source, "lxml")
            browser.quit()
        table = soup.findChildren('tr')
        leaderboard_list = ['test', 'test2']
        for child in table:
            child = child.findNext('a')
            child = str(child)
            user = child.split('>')[1]
            user = user.split('<')[0]
            user = user.lower()
            if user in leaderboard_list:
                pass
            elif len(leaderboard_list) < 20:
                leaderboard_list.append(user)
            else:
                pass
        with open(filename, "w") as leaderfile:
            for i in leaderboard_list:
                leaderfile.write(i + '\n')


def grabdata_all_crawl_sites():
    """Returns dict of players and site they are using"""

    url = "https://crawl.develz.org/watch.htm"
    browser = webdriver.PhantomJS()
    browser.get(url)
    time.sleep(1)  # Maybe can do, While soup is false (empty), then when true,
# continue?
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
        user_dict[user] = site
    return user_dict


LEADERBOARDS = Leaderboards('http://crawl.akrasiac.org/scoring/streaks.html',
                            'top_streak.txt')
LEADERBOARDS_FILE = Path('./' + LEADERBOARDS.filename)
if LEADERBOARDS_FILE.is_file():
    print('Leaderbord file found.')
else:
    print('No Leaderboard file found, creating one...')
    Leaderboards.grab_leaderboard_data(LEADERBOARDS)

with open(LEADERBOARDS.filename, "r") as afile:
    TEMP_TOP_PLAYERS = afile.read()
TOP_PLAYERS = (TEMP_TOP_PLAYERS.rstrip('\n')).splitlines()
ACTIVE_PLAYERS = grabdata_all_crawl_sites()

FOUND_PLAYERS = []
for top_player in TOP_PLAYERS:
    if top_player in ACTIVE_PLAYERS:
        FOUND_PLAYERS.append(top_player)
        print('Player:', top_player, '- Site:', ACTIVE_PLAYERS[top_player])
if not FOUND_PLAYERS:
    print('No Top Players Found')
