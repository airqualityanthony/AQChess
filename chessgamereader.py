import chess
import chess.pgn

def get_results(file, user, opponent):
    pgn = open(file)

    # set up games list
    games = []

    # read all games in pgn file
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break  # end of file

        games.append(game)
    
    results = []
    # loop through games files and check if user is present in white or black and return result.
    for i in range(0,len(games)):   
        if user in games[i].headers['White'] and opponent in games[i].headers['Black']:
            results.append((games[i].headers['White'],games[i].headers['Result'],games[i].headers['Black']))
        if user in games[i].headers['Black'] and opponent in games[i].headers['White']:
            results.append((games[i].headers['White'],games[i].headers['Result'],games[i].headers['Black']))
    if len(results) >= 1:
        return results

