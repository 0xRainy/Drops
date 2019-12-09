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
parser.add_option('-v', '--verbose', dest='verbose',
                  help='1: Show chain path. 2: Show DB statistics. \
                  3: Show both.')
parser.add_option('--min', '--minlength', dest='min',
                  help='The minimum chain length')
parser.add_option('--max', '--maxlength', dest='max',
                  help='The maximum chain length')
parser.add_option('-t', '--tries', dest='tries',
                  help='The maximum number of attempts at building a chain')

(options, args) = parser.parse_args()

if options.channel is None:
    options.channel = input('Enter at least one channel name: ')

if options.mode is None:
    options.mode = 'a'

if options.perception is None:
    options.perception = 20

if options.min is None:
    options.min = 5

if options.max is None:
    options.max = 20

if options.tries is None:
    options.tries = 20

if options.verbose is None:
    options.verbose = 0


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
    chain = getChain(options.max)
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
    if int(options.verbose) == 2 or int(options.verbose) == 3:
        print(getChain(options.max), "\n")
        dictStat()
    else:
        print(getChain(options.max), "\n")


def getChain(length):
    global relative
    global lines
    chain = []
    loop = 1
    tries = 0
    path = []
    failed = []
    while loop == 1 and tries < int(options.tries):
        tries += 1
        if relative == 'r':
            chain.append(random.choice(words))
            mode = 'Relative'
        elif relative == 'a':
            chain.append(random.choice(list(mrkvdb.keys())))
            mode = 'Any'
        elif relative == 'sr':
            rstarters = []
            for line in lines:
                rstarter = line.split(' ', 1)
                if rstarter[0][0:1:] != '@':
                    rstarters.append(rstarter[0])
            chain.append(random.choice(rstarters))
            mode = 'Relative Starters'
        elif relative == 's':
            global starters
            for line in lines:
                starter = line.split(' ', 1)
                if starter[0][0:1:] != '@':
                    starters.append(starter[0])
            chain.append(random.choice(starters))
            mode = 'Starters'
        seed = chain[0]
        for i in range(int(length)-1):
            try:
                if mrkvdb.get(chain[i]):
                    path.append(mrkvdb.get(chain[i]))
                    link = random.choice(mrkvdb[chain[i]])
                    chain.append(link)
            except IndexError:
                break
                # print("Unable to build full chain: stopping at", i+1, "of",
                #       length, "words.")
        if len(chain) < int(options.min):
            failed.append(chain)
            chain = []
            seed = []
            path = []
        elif len(chain) >= int(options.min) or int(options.max):
            loop = 0
    lines = []
    print('\nMODE: ', mode)
    print('Perception: ', options.perception)
    if int(options.verbose) == 1 or int(options.verbose) == 3:
        print('Chain Start', '\n--------------')
    if len(chain) == 0:
        if int(options.verbose) == 1 or int(options.verbose) == 3:
            print('Failed Attempts:')
            print(*failed, sep="\n")
        print('----RESULT----')
        return('Failed to build chain of length ' + str(options.min) + ' in '
               + str(tries) + ' tries.')
    else:
        if int(options.verbose) == 1 or int(options.verbose) == 3:
            print('Seed: ', seed)
            print(*path, sep="\n")
        print('----RESULT in', tries, 'tries---')
        return(" ".join(chain))


def dictStat():
    print('----mrkvDB Stats----')
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
