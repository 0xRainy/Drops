import random
import sys
import os
from dotenv import load_dotenv
from twitchio.ext import commands


load_dotenv()
# length = sys.argv[1]
relative = sys.argv[2]
channel = [sys.argv[1]]
mrkvdb = {}
lines = []
newChain = ''

# twitch bot stuff
markovc = commands.Bot(
    irc_token=os.environ.get('TMI_TOKEN'),
    client_id=os.environ.get('CLIENT_ID'),
    nick=os.environ.get('BOT_NICK'),
    prefix=os.environ.get('BOT_PREFIX'),
    initial_channels=channel
)


@markovc.event
async def event_ready():
    'Called once when the bot comes online'
    print(f"Bot is online in", channel, "!")
    # ws = markovc._ws
    # await ws.send_privmsg('rainyy', f"/me is listening..")


@markovc.event
async def event_message(ctx):
    'Runs every time a message is sent in chat'
    if ctx.author.name.lower() == 'rainyy':
        return
    # await markovc.handle_commands(ctx)
    global lines
    global newChain
    lines.append(ctx.content)
    if len(lines) > 20:
        newChain = getChain(random.randint(5, 20))
        dictStat()
    else:
        # print(len(lines))
        sys.stdout.write("\r%d%s" % (len(lines), ' lines gathered'))
        sys.stdout.flush()


def getChain(length):
    global lines
    global relative
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

    chain = []
    if relative == 'r':
        chain.append(random.choice(words))
        print('\nRelative MODE')
    elif relative == 'a':
        chain.append(random.choice(list(mrkvdb.keys())))
    print('\nChain Start', '\n--------------')
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


@markovc.command(name='chain')
async def chain(ctx):
    chain = getChain(random.randint(5, 12))
    await ctx.send(chain)


def dictStat():
    print('----RESULT----', '\n', newChain, '\n----mrkvDB Stats----')
    print('# of Keys: ', len(mrkvdb.keys()))
    count = 0
    for key, value in mrkvdb.items():
        count += len(value)
    print('# of Values: ', count)
    print('mrkvDB length: ', len(mrkvdb)+count, ', mrkvDB size:',
           "%.3f" % (sys.getsizeof(mrkvdb) * (10 ** -6)),'MB')
    print('------------\n')
    # print('mrkvdb:')
    # sorted_dict = {i: sorted(j) for i, j in mrkvdb.items()}
    # for x in sorted_dict:
    #     print(repr(x), ":", sorted_dict[x])


# Run the bot
if __name__ == "__main__":
    markovc.run()
