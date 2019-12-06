""" A simple Markov chain twitch bot that can be a fun CLI tool or used as
    an actual chat bot.

    To setup the twitch bot, create an .env file with the following options:
        TMI_TOKEN=''
        CLIENT_ID=''
        BOT_NICK=''
        BOT_PREFIX=''
"""
import random
import sys
import os
import optparse
from dotenv import load_dotenv
from twitchio.ext import commands


# Options
parser = optparse.OptionParser()
parser.add_option('-m', '--mode', dest='mode',
                  help='Relative = r (chooses seed from last dbupdate list of words\
                          or Any = a (chooses any word in the db)[default]')
parser.add_option('-c', '--channel', dest='channel',
                  help='List of channels separated by commas')
parser.add_option('-p', '--perception', dest='perception',
                  help='Number of lines before db is updated and chain is\
                          printed')
parser.add_option('-v', '--verbose', action="store_true", dest='verbose',
                  help='Show DB statistics')

(options, args) = parser.parse_args()

if options.channel is None:
    options.channel = input('Enter at least one channel name: ')

if options.mode is None:
    options.mode = 'a'

if options.perception is None:
    options.perception = 20


# Globals
perception = int(options.perception)
relative = options.mode
channel = options.channel
mrkvdb = {}
lines = []
words = []
starters = []


# Twitch Bot Config
load_dotenv()
markovc = commands.Bot(
    irc_token=os.environ.get('TMI_TOKEN'),
    client_id=os.environ.get('CLIENT_ID'),
    nick=os.environ.get('BOT_NICK'),
    prefix=os.environ.get('BOT_PREFIX'),
    initial_channels=[channel]
)


@markovc.event
async def event_ready():
    'Called once when the bot comes online'
    print(f"Bot is online in", channel, "!")
    # ws = markovc._ws
    # await ws.send_privmsg(os.environ.get('BOT_NICK'), f"/me is listening..")


@markovc.event
async def event_message(ctx):
    'Runs every time a message is sent in chat'
    if ctx.author.name.lower() == os.environ.get('BOT_NICK'):
        return
    # await markovc.handle_commands(ctx)
    global lines
    lines.append(ctx.content)
    if len(lines) > perception:
        mrkvdbUpdate()
    else:
        sys.stdout.write("\r%d%s" % (len(lines), ' lines gathered'))
        sys.stdout.flush()


@markovc.command(name='chain')
async def chain(ctx):
    'Prints a Markov chain'
    chain = getChain(random.randint(5, 20))
    await ctx.send(chain)


def mrkvdbUpdate():
    global lines
    global words
    # print("lines", lines)
    for line in lines:
        words = line.split()
        for i in range(len(words)):
            if i+1 < len(words):
                pair = [words[i], words[i+1]]
                # print(pair)
                mrkvdb.setdefault(pair[0], []).append(pair[1])
            else:
                mrkvdb[words[i]] = []
    if options.verbose:
        dictStat()
    else:
        print('----RESULT----', '\n', getChain(random.randint(5, 20)))


def getChain(length):
    global relative
    global lines
    chain = []
    if relative == 'r':
        chain.append(random.choice(words))
        print('\nMODE: Relative')
    elif relative == 'a':
        chain.append(random.choice(list(mrkvdb.keys())))
        print('\nMODE: Any')
    elif relative == 'sr':
        rstarters = []
        for line in lines:
            rstarter = line.split(' ', 1)
            if rstarter[0][0:1:] != '@':
                rstarters.append(rstarter[0])
        chain.append(random.choice(rstarters))
        print('\nMODE: Relative Starters')
    elif relative == 's':
        global starters
        for line in lines:
            starter = line.split(' ', 1)
            if starter[0][0:1:] != '@':
                starters.append(starter[0])
        chain.append(random.choice(starters))
        print('\nMODE: Starters')

    print('Perception: ', options.perception)
    print('Chain Start', '\n--------------')
    print('Seed: ', chain)
    for i in range(length):
        print(mrkvdb.get(chain[i]))
        if mrkvdb.get(chain[i]):
            link = random.choice(mrkvdb[chain[i]])
            chain.append(link)
        else:
            print("Unable to build full chain: stopping at", i+1, "of",
                  length, "words.")
            break
    lines = []
    return(" ".join(chain))


def dictStat():
    print('----RESULT----', '\n', getChain(random.randint(5, 20)),
          '\n----mrkvDB Stats----')
    print('# of Keys: ', len(mrkvdb.keys()))
    count = 0
    for key, value in mrkvdb.items():
        count += len(value)
    print('# of Values: ', count)
    if options.mode == 's':
        print('# of starters: ', len(starters))
    print('mrkvDB length: ', len(mrkvdb)+count, ', mrkvDB size:',
          "%.3f" % (sys.getsizeof(mrkvdb) * (10 ** -6)), 'MB')
    print('------------\n')
    # print('mrkvdb:')
    # sorted_dict = {i: sorted(j) for i, j in mrkvdb.items()}
    # for x in sorted_dict:
    #     print(repr(x), ":", sorted_dict[x])


# Run the bot
if __name__ == "__main__":
    markovc.run()
