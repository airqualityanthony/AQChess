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
            elif i['White'] == user and i['W_Result'] == "draw":
                wins += 0.5
            elif i['Black'] == user and i['B_Result'] == "draw":
                wins += 0.5
            elif i['White'] == user and i['W_Result'] == "insufficient":
                wins += 0.5
            elif i['Black'] == user and i['B_Result'] == "insufficient":
                wins += 0.5
            
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
wins = win_list(user_list, month="04",year="2020")
pgn_list = games_return(user_list[0], month= "04",year="2020")
details = list(zip(names,user_list,wins))
ordered_details = sorted(details,key=lambda x:x[2], reverse = True)
# get PGN string for chess.js to read.
moves = []
game_details = []
for i in pgn_list:
    games = []
    pgn = io.StringIO(i)
    game = chess.pgn.read_game(pgn)
    move = str(game.mainline())
    moves.append(move)
    games.append(move)
    white_p = game.headers['White']
    black_p = game.headers['Black']
    date = game.headers['EndDate']
    time = game.headers['EndTime']
    dt = str(date + " " + time)
    games.append(white_p)
    games.append(black_p)
    games.append(dt)
    game_details.append(games)

names = ["Anthony","Josh","Pauls","Naval","Lee","Alex","James","Girish"]
user_list = ["ElectricFalcon", "JPeg71","paulsilzins","ChessWho1","ldavie2","mralexbarr","Relph29","HardAmmo"]
## front page game results
## march games ElectricFalcon - Need to do everyone, plus and remove duplicates
Anthony_games = games_list(games_return(user_list[0], month= "04",year="2020"))
Josh_games = games_list(games_return(user_list[1], month= "04",year="2020"))
Pauls_games = games_list(games_return(user_list[2], month= "04",year="2020"))
Naval_games = games_list(games_return(user_list[3], month= "04",year="2020"))
Lee_games = games_list(games_return(user_list[4], month= "04",year="2020"))
Alex_games = games_list(games_return(user_list[5], month= "04",year="2020"))
James_games = games_list(games_return(user_list[6], month= "04",year="2020"))
Girish_games = games_list(games_return(user_list[7], month= "04",year="2020"))

g = Anthony_games+Josh_games+Pauls_games+Naval_games+Lee_games+Alex_games+James_games+Girish_games
## remove duplicates
import itertools
g.sort()
new_num = list(num for num,_ in itertools.groupby(g))

Anthony_moves = games_return(user_list[0], month= "04",year="2020")
Josh_moves = games_return(user_list[1], month= "04",year="2020")
Pauls_moves = games_return(user_list[2], month= "04",year="2020")
Naval_moves = games_return(user_list[3], month= "04",year="2020")
Lee_moves = games_return(user_list[4], month= "04",year="2020")
Alex_moves = games_return(user_list[5], month= "04",year="2020")
James_moves = games_return(user_list[6], month= "04",year="2020")
Girish_moves = games_return(user_list[7], month= "04",year="2020")

g_moves = Anthony_moves+Josh_moves+Pauls_moves+Naval_moves+Lee_moves+Alex_moves+James_moves+Girish_moves
## remove duplicates
import itertools
g_moves.sort()
moves_clean = list(num for num,_ in itertools.groupby(g_moves))

games_total = []
for i in moves_clean:
    games = []
    pgn = io.StringIO(i)
    game = chess.pgn.read_game(pgn)
    move = str(game.mainline())
    games.append(move)
    white_p = game.headers['White']
    black_p = game.headers['Black']
    date = game.headers['EndDate']
    time = game.headers['EndTime']
    dt = str(date + " " + time)
    games.append(white_p)
    games.append(black_p)
    games.append(dt)
    games_total.append(games)


games_march = games_list(pgn_list)
details_march = list(zip(names,user_list,wins))

pgn_list_april = games_return(user_list[0], month= "04",year="2020")
details_april = list(zip(names,user_list,wins))
ordered_details_april = sorted(details_april,key=lambda x:x[2], reverse = True)
games_april = games_list(pgn_list_april)

latest_game = games_total[-1]
latest_game_moves = games_total[-1][0]

print(ordered_details)

@app.route("/")
def home():
	return render_template("index.html", details = ordered_details, games = new_num, latest_game = latest_game, latest_moves = latest_game_moves)
@app.route("/april")
def april():
    return render_template("april.html", details = ordered_details_april, games = new_num)

@app.route("/games")
def games():
	return render_template("games.html", moves = moves[0], details = game_details[0])

if __name__ == "__main__":
	app.run(debug = True)


 