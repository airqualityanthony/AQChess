from flask import Flask, redirect, url_for, render_template, request
import chess
import chess.pgn
import io
import requests
from operator import add

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

def win_list(users,month = "03",year="2020"):
    games = []

    for y in users:
        games.append(versus_check(y,month,year))

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


names = ["Anthony","Josh","Pauls","Naval","Lee","Alex","James","Girish"]
user_list = ["ElectricFalcon", "JPeg71","paulsilzins","ChessWho1","ldavie2","mralexbarr","Relph29","HardAmmo"]
## run win_list function to retrieve number of wins for each player.
wins_march = win_list(user_list, month="03",year="2020")
wins_april = win_list(user_list, month="04",year="2020")
wins = list(map(add,wins_march,wins_april))
pgn_list = games_return(user_list[0], month= "03",year="2020")
details = list(zip(names,user_list,wins))

# get PGN string for chess.js to read.
moves = []
for i in pgn_list:
    games = []
    pgn = io.StringIO(i)
    game = chess.pgn.read_game(pgn)
    move = str(game.mainline())
    games.append(move)
    white_p = game.headers['White']
    black_p = game.headers['Black']
    date = game.headers['EndDate']
    time = game.headers['EndTime']
    dt = str(date + time)
    games.append(white_p)
    games.append(black_p)
    games.append(dt)
    moves.append(games)

print(moves)

g = games_list(pgn_list)
games_march = games_list(pgn_list)
details_march = list(zip(names,user_list,wins))

pgn_list_april = games_return(user_list[0], month= "04",year="2020")
details_april = list(zip(names,user_list,wins))
games_april = games_list(pgn_list_april)


@app.route("/")
def home():
	return render_template("index.html", details = details, games = g)
@app.route("/march")
def march():
	return render_template("march.html", details = details_march, games = games_march)
@app.route("/april")
def april():
    return render_template("april.html", details = details_april, games = games_april)
# @app.route("/may")
# def may():
# 	return render_template("may.html", details = details, games = games)


@app.route("/games")
def games():
	return render_template("games.html", pgn = moves)

if __name__ == "__main__":
	app.run(debug = True)


 