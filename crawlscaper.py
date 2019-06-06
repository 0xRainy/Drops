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


def add_followers():
    """ Reads from file followed_players.txt and returns a list.
        Entries in followed_players.txt must be separated by new lines.
    """
    followers_file = Path(FOLLOWED_PLAYERS_FILE)
    if FOLLOWED_PLAYERS_FILE.is_file():
        with open(followers_file, "r") as bfile:
            temp_followed_players = bfile.read()
    followed_players = (temp_followed_players.rstrip('\n')).splitlines()
    return followed_players


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
    user_dict = {'test': 'testsite', 'test2': 'testsite2', 'gammafunk': 'testsite3', 'poop': 'testsite4', 'qooq': 'testsite5'}
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
FOLLOWED_PLAYERS_FILE = Path('./followed_players.txt')
LEADERBOARDS_FILE = Path('./' + LEADERBOARDS.filename)
FOLLOWED_PLAYERS_LIST = add_followers()

if LEADERBOARDS_FILE.is_file():
    print('Leaderbord file found.')
else:
    print('No Leaderboard file found, creating one...')
    Leaderboards.grab_leaderboard_data(LEADERBOARDS)

with open(LEADERBOARDS.filename, "r") as afile:
    TEMP_TOP_PLAYERS = afile.read()
TOP_PLAYERS = (TEMP_TOP_PLAYERS.rstrip('\n')).splitlines()

if FOLLOWED_PLAYERS_FILE.is_file():
    print('Followed Players file found.')
    print('Added ' + str(len(FOLLOWED_PLAYERS_LIST)) + ' players to watch list...')
else:
    print('No Followed Players file found, create one!')
    print('No Followed Players added to watch list!')

ACTIVE_PLAYERS = grabdata_all_crawl_sites()

FOUND_TOP_PLAYERS = []
for top_player in TOP_PLAYERS:
    if top_player in ACTIVE_PLAYERS:
        FOUND_TOP_PLAYERS.append(top_player)
if FOUND_TOP_PLAYERS:
    print('Found Leaderboard Players')
    print('-------------------------')
for top_player in FOUND_TOP_PLAYERS:
    print('Player:', top_player, '- Site:', ACTIVE_PLAYERS[top_player])
print('\n')
if not FOUND_TOP_PLAYERS:
    print('No Top Players Found')
    print('\n')

FOUND_FOLLOWED_PLAYERS = []
for followed_player in FOLLOWED_PLAYERS_LIST:
    if followed_player in ACTIVE_PLAYERS:
        FOUND_FOLLOWED_PLAYERS.append(followed_player)
if FOUND_FOLLOWED_PLAYERS:
    print('Found Followed Players')
    print('-------------------------')
for followed_player in FOUND_FOLLOWED_PLAYERS:
    print('Player:', followed_player, '- Site:', ACTIVE_PLAYERS[followed_player])
print('\n')
if not FOUND_FOLLOWED_PLAYERS:
    print('No Followed Players Found')
    print('\n')
