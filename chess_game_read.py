import requests

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


