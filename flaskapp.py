from flask import Flask, redirect, url_for, render_template, request
from AQChessLadder import win_list
from chess_game_read import games_return
import chess
import chess.pgn
import io

app = Flask(__name__)

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


 