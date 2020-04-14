from codecs import open
from datetime import date
import os.path
import requests

games = []
user = "ElectricFalcon"

def game_downloader(user):
    print("Downloading %s's games to %s:" % (user, user))
    try:
        os.mkdir(user)
    except: 
        print("folder exists, continuing")
    finally:  
        archives = []
        for archive in get('https://api.chess.com/pub/player/%s/games/archives' % user)['archives']:
            archives.append(archive)
        download_archive(archives[-1], user, user)

def get(url):
    return requests.get(url).json()


def download_archive(url, where, user):
    games = get(url)['games']
    d = date.fromtimestamp(games[0]['end_time'])
    y = d.year
    m = d.month
    user = user
    filename = os.path.join(where, "%d-%02d-%s.pgn" % (y, m, user))
    print('Starting work on %s...' % filename)
    # XXX: If a file with this name already exists, we'll blow away the old
    # one. Possibly not ideal.
    with open(filename, 'w', encoding='utf-8') as output:
        for game in games:
            print(game['pgn'], file=output)
            print('', file=output)

game = get('https://api.chess.com/pub/player/electricfalcon/games/2020/04')

games_list = []
for games in game['games']:
    games_list.append(games)    


for i in games_list:
    print(i.keys())


# MM = "02"
# YYYY = "2019"
# username = "ElectricFalcon"
# url = f"https://api.chess.com/pub/player/{username}/games/{YYYY}/{MM}"

# # chess = json.loads(requests.get(url).content)

# # for i in range(0,len(chess['games'])):
# #     games.append((chess['games'][i]['white']['username'],chess['games'][i]['black']['username'], chess['games'][i]['white']['result'],chess['games'][i]['black']['result']))

# def download_archive(url, where, user):
#     games = get(url)['games']
#     d = date.fromtimestamp(games[0]['end_time'])
#     y = d.year
#     m = d.month
#     user = user
#     filename = os.path.join(where, "%d-%02d-%s.pgn" % (y, m, user))
#     print('Starting work on %s...' % filename)
#     # XXX: If a file with this name already exists, we'll blow away the old
#     # one. Possibly not ideal.
#     with open(filename, 'w', encoding='utf-8') as output:
#         for game in games:
#             print(game['pgn'], file=output)
#             print('', file=output)

# # YYYY = "2019"
# # username = "electricfalcon"
# # url = f"https://api.chess.com/pub/player/{username}/games/{YYYY}/{months[0]}"

# # chess = json.loads(requests.get(url).content)

# # for i in range(0,len(chess['games'])):
# #     games.append((chess['games'][i]['white']['username'],chess['games'][i]['black']['username'], chess['games'][i]['white']['result'],chess['games'][i]['black']['result']))
# download_archive(url,username,username)
# # for i in range(0,len(games)):
# #     print(games[i])



