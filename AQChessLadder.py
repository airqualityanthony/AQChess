from chess_game_read import get, versus_check, win_check

users = ["ElectricFalcon", "JPeg71","paulsilzins","ChessWho1","ldavie2","mralexbarr","Relph29","HardAmmo"]

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


