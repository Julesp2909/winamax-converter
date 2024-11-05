
import sys
sys.path.append("/home/JPJokerman/mysite/website/")
from scrapping.get_league_odds import get_games



countries ={ "ge", "it", "en", "es", "fr"}


#### GET THE BEST GAMES (HIGH TRJ)
games=[]
for i in countries:
    games += (get_games(i))

sorted_games = sorted(games, key=lambda x: x['trj'], reverse=True)

sorted_games=sorted_games[:5]



### A team's odd must be lower than B team's odd

for game in sorted_games:

    if game['teamA_odd']>game['teamB_odd']:
        temp=game['teamB_odd']
        game['teamB_odd']=game['teamA_odd']
        game['teamA_odd']=temp
        temp=game['teamA_name']
        game['teamA_name']=game['teamB_name']
        game['teamB_name']=temp







##### 2 BEST GAMES


game1_team1 = sorted_games[0]['teamA_name']
game1_team2 = sorted_games[0]['teamB_name']
game1_draw = 'Draw'
game2_team1 = sorted_games[1]['teamA_name']
game2_team2 = sorted_games[1]['teamB_name']
game2_draw = 'Draw'

odds_team_1 = {
    'team1_odd': sorted_games[0]['teamA_odd'],
    'draw_odd': sorted_games[0]['draw_odd'],
    'team2_odd': sorted_games[0]['teamB_odd'],
}

odds_team_2 = {
    'team1_odd': sorted_games[1]['teamA_odd'],
    'draw_odd': sorted_games[1]['draw_odd'],
    'team2_odd': sorted_games[1]['teamB_odd'],
}











#### GET THE RATE AND THE ODDS

tab_odds = {
    'A1A2':(odds_team_1['team1_odd']*odds_team_2['team1_odd']),
    'A1N2':(odds_team_1['team1_odd']*odds_team_2['draw_odd']),
    'A1B2':(odds_team_1['team1_odd']*odds_team_2['team2_odd']),
    'N1A2':(odds_team_1['draw_odd']*odds_team_2['team1_odd']),
    'N1N2':(odds_team_1['draw_odd']*odds_team_2['draw_odd']),
    'N1B2':(odds_team_1['draw_odd']*odds_team_2['team2_odd']),
    'B1A2':(odds_team_1['team2_odd']*odds_team_2['team1_odd']),
    'B1N2':(odds_team_1['team2_odd']*odds_team_2['draw_odd']),
    'B1B2':(odds_team_1['team2_odd']*odds_team_2['team2_odd'])
}

name_tab ={
    'A1A2': f"{game1_team1} x {game2_team1}",
    'A1N2': f"{game1_team1} x {game2_draw}",
    'A1B2': f"{game1_team1} x {game2_team2}",
    'N1A2': f"{game1_draw} x {game2_team1}",
    'N1N2': f"{game1_draw} x {game2_draw}",
    'N1B2': f"{game1_draw} x {game2_team2}",
    'B1A2': f"{game1_team2} x {game2_team1}",
    'B1N2': f"{game1_team2} x {game2_draw}",
    'B1B2': f"{game1_team2} x {game2_team2}",
}

name_tab_teamA = {
    'A1A2': game1_team1,
    'A1N2': game1_team1,
    'A1B2':game1_team1,
    'N1A2': game1_draw,
    'N1N2': game1_draw,
    'N1B2': game1_draw,
    'B1A2': game1_team2,
    'B1N2': game1_team2,
    'B1B2': game1_team2
}

name_tab_teamB = {
    'A1A2': game2_team1,
    'A1N2': game2_draw,
    'A1B2':game2_team2,
    'N1A2': game2_team1,
    'N1N2': game2_draw,
    'N1B2': game2_team2,
    'B1A2': game2_team1,
    'B1N2': game2_draw,
    'B1B2': game2_team2
}


private_stake_real = 100
private_winning_real = private_stake_real*tab_odds['A1A2']

private_stake_freebets = {
    'A1N2':private_winning_real/(tab_odds['A1N2']-1),
    'A1B2':private_winning_real/(tab_odds['A1B2']-1),
    'N1A2':private_winning_real/(tab_odds['N1A2']-1),
    'N1N2':private_winning_real/(tab_odds['N1N2']-1),
    'N1B2':private_winning_real/(tab_odds['N1B2']-1),
    'B1A2':private_winning_real/(tab_odds['B1A2']-1),
    'B1N2':private_winning_real/(tab_odds['B1N2']-1),
    'B1B2':private_winning_real/(tab_odds['B1B2']-1)
}

private_stake_freebets_total = sum(private_stake_freebets.values())
private_overall_winnings = private_winning_real-private_stake_real




##############################

##############################


def public_stake_real(freebets):
    public_stake = private_stake_real*(freebets/private_stake_freebets_total)
    return public_stake

def public_winnings_real(freebets):
    a = public_stake_real(freebets)*tab_odds['A1A2']

    return a

def public_stake_freebets(freebets):
    real_winning = public_winnings_real(freebets)
    stake_tab = {
        'A1A2':public_stake_real(freebets),
        'A1N2':real_winning/(tab_odds['A1N2']-1),
        'A1B2':real_winning/(tab_odds['A1B2']-1),
        'N1A2':real_winning/(tab_odds['N1A2']-1),
        'N1N2':real_winning/(tab_odds['N1N2']-1),
        'N1B2':real_winning/(tab_odds['N1B2']-1),
        'B1A2':real_winning/(tab_odds['B1A2']-1),
        'B1N2':real_winning/(tab_odds['B1N2']-1),
        'B1B2':real_winning/(tab_odds['B1B2']-1)
    }
    return stake_tab



def public_winnings_freebets(freebets):
    winnings_tab = {
        'A1A2': public_winnings_real(freebets),
        'A1N2':(public_stake_freebets(freebets)['A1N2'])*(tab_odds['A1N2'])-(public_stake_freebets(freebets)['A1N2']),
        'A1B2':(public_stake_freebets(freebets)['A1B2'])*(tab_odds['A1B2'])-(public_stake_freebets(freebets)['A1B2']),
        'N1A2':(public_stake_freebets(freebets)['N1A2'])*(tab_odds['N1A2'])-(public_stake_freebets(freebets)['N1A2']),
        'N1N2':(public_stake_freebets(freebets)['N1N2'])*(tab_odds['N1N2'])-(public_stake_freebets(freebets)['N1N2']),
        'N1B2':(public_stake_freebets(freebets)['N1B2'])*(tab_odds['N1B2'])-(public_stake_freebets(freebets)['N1B2']),
        'B1A2':(public_stake_freebets(freebets)['B1A2'])*(tab_odds['B1A2'])-(public_stake_freebets(freebets)['B1A2']),
        'B1N2':(public_stake_freebets(freebets)['B1N2'])*(tab_odds['B1N2'])-(public_stake_freebets(freebets)['B1N2']),
        'B1B2':(public_stake_freebets(freebets)['B1B2'])*(tab_odds['B1B2'])-(public_stake_freebets(freebets)['B1B2']),
    }
    return winnings_tab

def public_stake_freebets_total(freebets):
    # SHOULD BE EQUAL TO THE AMOUNT OF FREEBETS
    sum_stake = sum(public_stake_freebets(freebets))
    return sum_stake


def public_overall_winnings(freebets):
    sum_winnings = public_winnings_real(freebets)-public_stake_real(freebets)
    return sum_winnings

def convert_rate(freebets):
    rate = 100*public_overall_winnings(freebets)/freebets
    return rate


####################################
## Le TABLEAU RENVOYÉ SUR DISCORD ##
def format_stake_tab(freebets):
    try:
        odds_name = list(tab_odds)
        stakes = public_stake_freebets(freebets)
        winnings = public_winnings_freebets(freebets)
        games_text = f"Games : **{game1_team1}** x **{game1_team2}** & **{game2_team1}** x **{game2_team2}**\nRate : {round(public_convert_rate(freebets), 2)}%\n\nRetour : {round((freebets*public_convert_rate(freebets))/100, 2)}€\n\n"

        odds_lines = games_text


        for i in odds_name:
            #Argent réel
            if game1_team1 == name_tab_teamA[i] and game2_team1 == name_tab_teamB[i]:
                odds_lines += f"__**{name_tab[str(i)]}**__ : **{round(stakes[i], 2)}€**  \nOdd : {round(tab_odds[str(i)], 2)} - Winnings : {round(winnings[i], 2)}€ - *Argent réel*\n\n---------\n"
            #Freebets
            else:
                odds_lines += f"__**{name_tab[str(i)]}**__ : **{round(stakes[i], 2)}€**  \nOdd : {round(tab_odds[str(i)], 2)} - Winnings : {round(winnings[i], 2)}€ - *Freebets*\n\n---------\n"


        return odds_lines
    except:
        pass
##############################

def public_convert_rate(freebets):
    rate = 100*public_overall_winnings(freebets)/freebets
    return rate


