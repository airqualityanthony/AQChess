from flask import Flask, redirect, url_for, render_template, request
import chess
import chess.pgn
import io
import requests

app = Flask(__name__)

def get(url):
    return requests.get(url).json()

def versus_check(user,month = "03",year = "2020"):
    users = ["ElectricFalcon", "JPeg71","paulsilzins","ChessWho1","ldavie2","mralexbarr","Relph29","HardAmmo"]
    if user in users: 
        users.remove(user)
    game = get(f'https://api.chess.com/pub/player/{user}/games/{year}/{month}')

    games_list = []
    for games in game['games']:
        games_list.append(games)    
    
    results = []    
    for x in users:
        for i in games_list:
            if user in i['white']['username'] and x in i['black']['username']:
                results.append({'White':i['white']['username'],"W_Result":i['white']['result'],"Black":i['black']['username'],"B_Result":i['black']['result']})
            if x in i['white']['username'] and user in i['black']['username']:
                results.append({'White':i['white']['username'],"W_Result":i['white']['result'],"Black":i['black']['username'],"B_Result":i['black']['result']})
    return(results)

def win_check(user,games):
    wins = 0
    for i in games: 
        if i is not None:  
            if i['White'] == user and i['W_Result'] == "win":
                wins += 1
            elif i['Black'] == user and i['B_Result'] == "win":
                wins += 1
        else:
            pass
    return(wins)

def games_return(user,month = "03",year = "2020"):
    users = ["ElectricFalcon", "JPeg71","paulsilzins","ChessWho1","ldavie2","mralexbarr","Relph29","HardAmmo"]
    if user in users: 
        users.remove(user)
    game = get(f'https://api.chess.com/pub/player/{user}/games/{year}/{month}')

    games_list = []
    for games in game['games']:
        games_list.append(games)    
    
    results = []    
    for x in users:
        for i in games_list:
            if user in i['white']['username'] and x in i['black']['username']:
                results.append(i['pgn'])
            if x in i['white']['username'] and user in i['black']['username']:
                results.append(i['pgn'])
    return(results)

def win_list(users):
    games = []

    for y in users:
        games.append(versus_check(y))

    wins = []
    for x in users:
        score = []
        for i in games:
            score.append(win_check(x,i))
        wins.append(score)
    final_scores = []
    for i in wins:
        x = max(i)
        final_scores.append(x)
    return(final_scores)

names = ["Anthony","Josh","Pauls","Naval","Lee","Alex","James","Girish"]
user_list = ["ElectricFalcon", "JPeg71","paulsilzins","ChessWho1","ldavie2","mralexbarr","Relph29","HardAmmo"]
## run win_list function to retrieve number of wins for each player.
wins = win_list(user_list)


pgn_list = games_return(user_list[0])
details = list(zip(names,user_list,wins))

## get PGN string for chess.js to read.
pgn = io.StringIO(pgn_list[0])
game = chess.pgn.read_game(pgn)
moves = str(game.mainline())
white = game.headers['White']
black = game.headers['Black']

def games_list(pgn_list):
	games = []
	for i in pgn_list:
		detail = []
		pgn = io.StringIO(i)
		game = chess.pgn.read_game(pgn)
		detail.append(game.headers['White'])
		detail.append(game.headers['Black'])
		detail.append(game.headers['Result'])
		detail.append(game.headers['EndDate'])
		detail.append(game.headers['EndTime'])
		detail.append(game.headers['Link'])
		games.append(detail)
	return(games)

g = games_list(pgn_list)


@app.route("/")
def home():
	return render_template("index.html", details = details, games = g)

@app.route("/games")
def games():
	return render_template("games.html", pgn = moves, white = white, black = black)

if __name__ == "__main__":
	app.run(debug = True)


 