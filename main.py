import requests
import json
import time

from lxml import html
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import steam.webauth as wa


def parcer(gameId: int = 730,
           min_price: int = 0,
           max_price: int = 10000000,
           sort: str = 'Popularity',
           limit: int = 1000000) -> dict:
    """
    :param: min_price - Minimal item price
    :param: max_price - Max item price
    :param: sort - Sorting type (Popularity, ) 
    """

    data = {}

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7 '
    }

    response = requests.get(
        f'https://tradeit.gg/api/v2/inventory/data?gameId={str(gameId)}&limit={str(limit)}&sortType={sort}&searchValue=&minPrice={str(min_price)}&maxPrice={str(max_price)}&minFloat=0&maxFloat=1&showTradeLock=true&colors=&showUserListing=true&fresh=false', headers=headers).json()

    with open('data.json', 'w') as f:
        for i in response['items']:
            try:
                id = i['id']
                _ = {i['id']: {'Name': i['name'], 'ID': id,
                               'Condition': i['steamTags'][5],
                               'Type': i['steamTags'][0],
                               'Price': i['price']/100,
                               'Count': response['counts'][str(id)]}}
                data.update(_)

            except KeyError:
                pass
        json.dump(data, f)

    return data





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


def parse_cinv():
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7 '
    }
    login_header = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'ru',
        'Referer' : 'https://steamcommunity.com/',
        'Accept-Encoding' : 'gzip, deflate, br',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15'
    }
    session = steam_login(LOGIN='', PASSWORD='')

    temp_html = session.get('https://connect-tradeit.com/auth/steam?sendTo=https://tradeit.gg/api/v2/steam/login', headers=headers).content
    soup = BeautifulSoup(temp_html)
    data = {'action':soup.find('input', {'name':'action'}).get('value'),
            'openid.mode':soup.find('input', {'name':'openid.mode'}).get('value'),
            'opeindparams':soup.find('input', {'name':'openidparams'}).get('value'),
            'nonce':soup.find('input', {'name':'nonce'}).get('value')}
    
    
    
    #print(session.post(f'https://steamcommunity.com/openid/login?action={openid_action}&openid.mode={openid_mode}&openidparams={openid_params}&nonce={openid_nonce}', headers=headers).content)
    session.post('https://steamcommunity.com/openid/login', json=data)
    my_items = session.get('https://tradeit.gg/api/v2/inventory/my/data?gameId=753&fresh=0', headers=headers).content
    print(my_items)
    


parse_cinv()
