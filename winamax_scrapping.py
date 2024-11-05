import requests
import json


# 5 major leagues - we can add every league, if listed on winamax
leagues_country_code = {
    'fr': '1/7/4',
    'it': '1/31/33',
    'es': '1/32/36',
    'ge':'1/30/42',
    'en': '1/1/1'
    }


def get_page(country: str):
    url_france= f"https://www.winamax.fr/paris-sportifs/sports/{leagues_country_code[country]}"
    
    response = requests.get(url_france, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0"})
    html = response.text
    return html


#### get the JSON, that includes the games/odds...
def get_json(country):
    html = get_page(country)
    
    split1 = html.split("var PRELOADED_STATE = ")[1]
    split2= split1.split(";</script>")[0]
    
    return json.loads(split2)


print(get_json('fr'))