
from .conversion_freebets import 
#from winamax_scrapping import get_json
#check if the league is correct
category_ids = {
    'fr': 7,
    'it':31,
    'es': 32,
    'ge':30,
    'en': 1
    }



def get_games(country):
    games=[]
    json = get_json(country)
    outcomes=[]
    for game in json['matches']:


        if (json['matches'][game]['sportId']!= 1 or json['matches'][game]['categoryId'] != category_ids[country] or json['matches'][game]['status']!='PREMATCH'):

            continue

        # Search into JSON
        try:
            bet_id = json['matches'][game]['mainBetId']

            tournament_id = json['matches'][game]['tournamentId']

            bet=json['bets'][str(bet_id)]['outcomes']

            tournament_name = json['tournaments'][str(tournament_id)]["tournamentName"]

            if (len(bet) != 3 ):
                continue

            convert_str_bet0 = str(bet[0])
            convert_str_bet1 = str(bet[1])
            convert_str_bet2 = str(bet[2])


            ## Keys

            teamA_name = json['matches'][game]['competitor1Name']

            draw_name = 'draw'

            teamB_name = json['matches'][game]['competitor2Name']

            teamA_odd = json['odds'][convert_str_bet0]

            draw_odd = json['odds'][convert_str_bet1]

            teamB_odd = json['odds'][convert_str_bet2]

            league = tournament_name

            trj = 100/((1/(teamA_odd))+(1/(draw_odd))+(1/(teamB_odd)))
        except:
            pass
        game_all_data = {
            'teamA_name': teamA_name,
            'draw_name': draw_name,
            'teamB_name': teamB_name,
            'teamA_odd': teamA_odd,
            'draw_odd': draw_odd,
            'teamB_odd': teamB_odd,
            'trj': trj,
            'league':league,
            ## The team with the lowest odd has to be first. If teamB_odd is lower than teamA's, then we switch these two team.
            'teamA_name_unsorted': teamA_name,
            'teamB_name_unsorted': teamB_name,
            'teamA_odd_unsorted': teamA_odd,
            'teamB_odd_unsorted': teamB_odd,

        }



        outcomes.append(game_all_data)
        ## CHECK THAT NO NONE VALUE IS IN THE LIST
    outcomes = [game for game in outcomes if None not in game]

    return list(outcomes)



















