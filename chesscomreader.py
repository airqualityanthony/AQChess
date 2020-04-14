from codecs import open
from datetime import date
import os.path
import requests

def game_downloader(user):
    print("Downloading %s's games to %s:" % (user, user))
    try:
        os.mkdir(user)
    except: 
        print("folder exists, continuing")
    finally:  
        for archive in get('https://api.chess.com/pub/player/%s/games/archives' % user)['archives']:
            download_archive(archive, user, user)

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

def get(url):
    return requests.get(url).json()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Download a user's games from chess.com")
    parser.add_argument('user', metavar='USER', help='The user whose games we want')
    args = parser.parse_args()
    game_downloader(args.user)