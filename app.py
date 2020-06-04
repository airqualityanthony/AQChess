from flask import Flask, redirect, url_for, render_template, request
import chess
import chess.pgn
import io
import requests
from operator import add
import itertools
import re

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
wins_april = win_list(user_list, month="04",year="2020")
wins_may = win_list(user_list, month="05",year="2020")
wins_june = win_list(user_list, month="06",year="2020")
wins_interim = map(add,wins_april,wins_may)
wins = list(map(add,wins_interim,wins_june))
## number of games
def number_of_games(user_list,month,year):
    g = []
    for i in user_list:
        g.append(len(games_list(games_return(i,month,year))))
    return(g)

april_num = number_of_games(user_list,"04","2020")
may_num = number_of_games(user_list,"05","2020")
jun_num = number_of_games(user_list,"06","2020")
num_games_interim = map(add,april_num,may_num)
num_games = list(map(add,num_games_interim,jun_num))

# print(len(games_list(games_return(user_list[0], "05","2020"))) + len(games_list(games_return(user_list[0], "04","2020"))))
details = list(zip(names,user_list,wins,num_games))
ordered_details = sorted(details,key=lambda x:x[2], reverse = True)



## front page game results
def games_list_total(month,year):
    Anthony_games = games_list(games_return(user_list[0], month,year))
    Josh_games = games_list(games_return(user_list[1], month,year))
    Pauls_games = games_list(games_return(user_list[2], month,year))
    Naval_games = games_list(games_return(user_list[3], month,year))
    Lee_games = games_list(games_return(user_list[4], month,year))
    Alex_games = games_list(games_return(user_list[5], month,year))
    James_games = games_list(games_return(user_list[6], month,year))
    Girish_games = games_list(games_return(user_list[7], month,year))
    g = Anthony_games+Josh_games+Pauls_games+Naval_games+Lee_games+Alex_games+James_games+Girish_games
    g.sort()
    new_num = list(num for num,_ in itertools.groupby(g))
    return(new_num)

new_num = games_list_total("04","2020") + games_list_total("05","2020") + games_list_total("06","2020")
ordered_new_num = sorted(new_num,key=lambda x:x[3], reverse = True)

def move_list_total(month,year):
    Anthony_moves = games_return(user_list[0], month,year)
    Josh_moves = games_return(user_list[1], month,year)
    Pauls_moves = games_return(user_list[2], month,year)
    Naval_moves = games_return(user_list[3], month,year)
    Lee_moves = games_return(user_list[4], month,year)
    Alex_moves = games_return(user_list[5], month,year)
    James_moves = games_return(user_list[6], month,year)
    Girish_moves = games_return(user_list[7], month,year)
    g_moves = Anthony_moves+Josh_moves+Pauls_moves+Naval_moves+Lee_moves+Alex_moves+James_moves+Girish_moves
    g_moves.sort()
    moves_clean = list(num for num,_ in itertools.groupby(g_moves))
    return(moves_clean)

moves_clean = move_list_total("04","2020") + move_list_total("05","2020") + move_list_total("06","2020")

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

latest_game = games_total[-1]
latest_game_moves = games_total[-1][0]

pgn = io.StringIO(latest_game_moves)
game = chess.pgn.read_game(pgn)
san_moves = []
board = chess.Board()

for move in game.mainline_moves():
    san_moves.append(board.san(move))
    board.push(move)

moves_table = [san_moves[x:x+2] for x in range(0, len(san_moves), 2)]
for i in moves_table:
    i.append(moves_table.index(i)+1)

@app.route("/")
def home():
	return render_template("index.html", details = ordered_details, games = ordered_new_num, latest_game = latest_game, latest_moves = latest_game_moves, pgn = moves_table)

if __name__ == "__main__":
	app.run(debug = True)


 