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


class Scraper():
    """Sets up the webdriver and scraper.
    """
    def __init__(self, url='', table='', tabledata=None):
        self.url = url
        self.table = table
        self.tabledata = tabledata
        coptions = webdriver.ChromeOptions()
        coptions.add_argument('--ignore-certificate-errors')
        coptions.add_argument('--incognito')
        coptions.add_argument('--headless')
        self.driver = webdriver.Chrome(options=coptions)

    def browser_get(self):
        """Spawns a hidden browser to scrape data from a dynamic
           website using JavaScript.
        """
        self.driver.get(self.url)
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        self.driver.quit()
        self.tabledata = soup.findChildren(self.table)


class Leaderboards():
    """Handles choosing a leaderboard to download data from.
       The filename parameter must include *.txt
    """
    def __init__(self, leaderboard_url='', filename=''):
        self.leaderboard_url = leaderboard_url
        self.filename = filename

    def grab_leaderboard_data(self):
        """Downloads leaderbord data from leaderboard_url and outputs
           formatted list to file separated by newline.
        """
        filename = self.filename
        url = self.leaderboard_url
        leader_table = Scraper(url, 'tr')
        leader_table.browser_get()
        leaderboard_list = []
        for child in leader_table.tabledata:
            child = child.findNext('a')
            child = str(child)
            user = child.split('>')[1]
            user = user.split('<')[0]
            if user in leaderboard_list:
                pass
            elif len(leaderboard_list) < 20:
                leaderboard_list.append(user)
            else:
                pass
        with open('./leaderboards/' + filename, "w") as leaderfile:
            for i in leaderboard_list:
                leaderfile.write(i + '\n')


def add_followers():
    """ Reads from file followed_players.txt and returns a list.
        Entries in followed_players.txt must be separated by new lines.
    """
    followers_file = Path(FOLLOWED_PLAYERS_FILE)
    if not FOLLOWED_PLAYERS_FILE.is_file():
        print('No Followers File found.. Creating one..')
        with open('followed_players.txt', "w") as followedplayers:
            followedplayers.write('')
        with open(followers_file, "r") as bfile:
            temp_followed_players = bfile.read()
    else:
        with open(followers_file, "r") as bfile:
            temp_followed_players = bfile.read()
    followed_players = (temp_followed_players.rstrip('\n')).splitlines()
    return followed_players


def grab_data_all_crawl_sites():
    """Returns dict of players and site they are using
    """
    url = 'https://crawl.develz.org/watch.htm'
    user_table = Scraper(url, 'tr')
    Scraper.browser_get(user_table)
    user_dict = {}
    for child in user_table.tabledata:
        child = child.findNext('a')
        child = str(child)
        site = child.split('"')[1]
        site = site.split('"')[0]
        if site == 'crawl.project357.org':
            user = child.split('h/')[1]
        else:
            user = child.split('-')[-1]
        user = user.split('"')[0]
        user_dict[user] = site
    return user_dict


LEADERBOARDS_DIR = Path('./leaderboards/')


if not Path.is_dir(LEADERBOARDS_DIR):
    Path.mkdir(LEADERBOARDS_DIR)
elif Path.is_dir(LEADERBOARDS_DIR):
    pass

LEADERBOARDS = {Leaderboards('http://crawl.akrasiac.org/scoring/streaks.html',
                             'top_streak.txt'): 'top_streak.txt',
                Leaderboards(
                    'https://crawl.develz.org/tournament/0.23/all-players.html',
                    'latest_tournament_players.txt'): 'latest_tournament_players.txt'}
FOLLOWED_PLAYERS_FILE = Path('followed_players.txt')
# LEADERBOARDS_FILES = []
# LEADERBOARDS_FILES.extend(list(LEADERBOARDS.values()))
# print(LEADERBOARDS_FILES)
FOLLOWED_PLAYERS_LIST = add_followers()
TEMP_TOP_PLAYERS = []
TOP_PLAYERS = []
RUN_ONCE = 0
for item in list(LEADERBOARDS.values()):
    leadersfile = Path('./leaderboards/' + item)
    if not leadersfile.is_file():
        if RUN_ONCE == 1:
            pass
        else:
            RUN_ONCE += 1
            print('No Leaderboard files found, creating them..')
        for lboard in LEADERBOARDS:
            lboard.grab_leaderboard_data()
            print('Created ' + LEADERBOARDS[lboard])
    else:
        print('Leaderbord file ' + item + ' found.')
for item in list(LEADERBOARDS.values()):
    with open('./leaderboards/' + item, "r") as afile:
        TEMP_TOP_PLAYERS.append(afile.read())
for player in TEMP_TOP_PLAYERS:
    TOP_PLAYERS.extend(player.rstrip('\n').splitlines())
TOP_PLAYERS = set(TOP_PLAYERS)
#TOP_PLAYERS.extend([player.rstrip('\n').splitlines() for
#                    player in TEMP_TOP_PLAYERS])

if FOLLOWED_PLAYERS_FILE.is_file():
    print('Followed Players file found.')
    print('Added ' + str(len(FOLLOWED_PLAYERS_LIST))
          + ' players to watch list...')
else:
    print('No Followed Players added to watch list!')

ACTIVE_PLAYERS = grab_data_all_crawl_sites()
FOUND_TOP_PLAYERS = []
for top_player in TOP_PLAYERS:
    if top_player in list(ACTIVE_PLAYERS.keys()):
        FOUND_TOP_PLAYERS.append(top_player)
if FOUND_TOP_PLAYERS:
    print('Found Top 50 Leaderboard Players')
    print('-------------------------')
for top_player in FOUND_TOP_PLAYERS:
    print('Player:', top_player, '- Site:', ACTIVE_PLAYERS[top_player], '\n')
if not FOUND_TOP_PLAYERS:
    print('No Top Players Found', '\n')

FOUND_FOLLOWED_PLAYERS = []
for followed_player in FOLLOWED_PLAYERS_LIST:
    if followed_player in ACTIVE_PLAYERS:
        FOUND_FOLLOWED_PLAYERS.append(followed_player)
if FOUND_FOLLOWED_PLAYERS:
    print('Found Followed Players')
    print('-------------------------')
for followed_player in FOUND_FOLLOWED_PLAYERS:
    print('Player:', followed_player, '- Spectate:',
          ACTIVE_PLAYERS[followed_player])
print('\n')
if not FOUND_FOLLOWED_PLAYERS:
    print('No Followed Players Found')
    print('\n')
