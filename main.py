import requests
import json
from urllib.parse import unquote, quote

from bs4 import BeautifulSoup
import steam.webauth as wa

def sinv_parcer(gameId: int = 730,
           min_price: int = 0,
           max_price: int = 1000,
           min_float: float = 0.0,
           max_float: float = 1.0,
           sort: str = 'Popularity',
           limit: int = 1000000,
           show_users_listings: bool = True,
           show_trade_lock: bool = True,
           ) -> dict:
    """
    :param: min_price - Min item price
    :param: max_price - Max item price
    :param: sort - Sorting type (Popularity, Release+Date, ) 
    """

    sinv = {}
    
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ', 
        'accept': '*/*'
    }


    if min_float == 0.0 and max_float == 1.0:
        min_float = int(min_float)
        max_float = int(max_float)
    response = requests.get(f'https://tradeit.gg/api/v2/inventory/data?gameId={str(gameId)}&limit={str(limit)}&sortType={sort}&searchValue=&minPrice={str(min_price)}&maxPrice={str(max_price)}&minFloat={str(min_float)}&maxFloat={str(max_float)}&showTradeLock={str(show_trade_lock).lower()}&colors=&showUserListing={str(show_users_listings).lower()}&fresh=false', headers=headers).json()
    
    with open('bot_data.json', 'w') as f:
        for i in response['items']:
            try:
                id = i['id']
                _ = {i['id']: {'Name': i['name'], 'ID': id,
                               'Condition': i['steamTags'][5],
                               'Type': i['steamTags'][0],
                               'Price': i['price']/100,
                               'Count': response['counts'][str(id)]}}
                sinv.update(_)

            except KeyError:
                pass
        json.dump(sinv, f)

    return sinv

# UNRELEASED DO NOT USE IT
def bot_item(game_id:int = None, 
             limit: int = None,
             sort_type: str = None, 
             item_name: int = None):
    
    url = 'https://tradeit.gg/api/v2/inventory/data?'

    if game_id:
        url += f'gameId={game_id}&'
    else:
        url += f'gameId=730'

    if limit:
        url += f'limit={limit}&'
    else:
        url += f'limit=10000000&'
    
    if sort_type != 'Popularity':
        url += f'sortType={sort_type}&'
    else:
        url += f'sortType=Popularity&'

    if item_name:
        url += f'SearchValue={quote(item_name)}&'
    else:
        url += f'SearchValue=&'
    
        

    data = {}
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7 '
    }
    
    response = requests.get(f'https://tradeit.gg/api/v2/inventory/data?gameId=730&offset=0&limit=500&sortType=Popularity&searchValue=&minPrice=0'
                            f'&maxPrice=100000&minFloat=0&maxFloat=1&showTradeLock=true&colors=&showUserListing=true&fresh=true', headers=headers).json()


def steam_cli_login(LOGIN: str, PASSWORD: str) -> requests.Session:
    user = wa.WebAuth(LOGIN)
    session = user.cli_login(PASSWORD)
    return session


def steam_login(LOGIN: str, PASSWORD: str) -> requests.Session:
    user = wa.WebAuth(LOGIN)

    if user.logged_on == True:
        session = user.session
        return session

    try:
        session = user.login(PASSWORD)

    except wa.EmailCodeRequired:
        email_code = input('EMail code: ')
        session = user.login(email_code=email_code)
    except wa.TwoFactorCodeRequired:
        twoFA = input('2FA: ')
        session = user.login(twofactor_code=twoFA)

    return session


def cinv_parser():
    cinv = {}

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7 '
    }
    
    session = steam_login(LOGIN='jaksonfeed', PASSWORD='jesus1337christT')

    temp_html = session.get('https://connect-tradeit.com/auth/steam?sendTo=https://tradeit.gg/api/v2/steam/login', headers=headers).content
    soup = BeautifulSoup(temp_html, features='lxml')
    data = {
    'action': (None, soup.find('input', {'id': 'actionInput'})['value']),
    'openid.mode': (None, soup.find('input', {'name': 'openid.mode'})['value']),
    'openidparams': (None, soup.find('input', {'name': 'openidparams'})['value']),
    'nonce': (None, soup.find('input', {'name': 'nonce'})['value'])
        }   
        
    session.post('https://steamcommunity.com/openid/login', files=data, headers=headers).content
    my_items = session.get('https://tradeit.gg/api/v2/inventory/my/data?gameId=730&fresh=0', headers=headers).json()
    del session
    with open('cinv_data.json', 'w') as f:
        for key, value in my_items['items'].items():
            for j in value:
                if key == 0:
                    continue
                else:
                    try:
                        id = j['id']
                        _ = {j['id']: {'Name': j['name'], 'ID': id,
                                    'Condition': j['steamTags'][5],
                                    'Type': j['steamTags'][0],
                                    'Price': j['price']/100}}
                        cinv.update(_)

                    except KeyError:
                        pass

        json.dump(cinv, f)

    return data