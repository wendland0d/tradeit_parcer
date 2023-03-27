import requests
import json
import time

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

    session = steam_login(LOGIN='steam_login', PASSWORD='steam_password')
    session.get('https://steamcommunity.com/openid/login?openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1&openid.sreg.optional=nickname%2Cemail%2Cfullname%2Cdob%2Cgender%2Cpostcode%2Ccountry%2Clanguage%2Ctimezone&openid.ns.ax=http%3A%2F%2Fopenid.net%2Fsrv%2Fax%2F1.0&openid.ax.mode=fetch_request&openid.ax.type.fullname=http%3A%2F%2Faxschema.org%2FnamePerson&openid.ax.type.firstname=http%3A%2F%2Faxschema.org%2FnamePerson%2Ffirst&openid.ax.type.lastname=http%3A%2F%2Faxschema.org%2FnamePerson%2Flast&openid.ax.type.email=http%3A%2F%2Faxschema.org%2Fcontact%2Femail&openid.ax.required=fullname%2Cfirstname%2Clastname%2Cemail&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.return_to=https%3A%2F%2Fconnect-tradeit.com%2Fauth%2Fsteam%2Freturn%3FsendTo%3Dhttps%3A%2F%2Ftradeit.gg%2Fapi%2Fv2%2Fsteam%2Flogin&openid.realm=https%3A%2F%2Fconnect-tradeit.com%2F', headers=headers)
    session.get('https://connect-tradeit.com/auth/steam/return?sendTo=https://tradeit.gg/api/v2/steam/login&openid.ns=http://specs.openid.net/auth/2.0&openid.mode=id_res&openid.op_endpoint=https://steamcommunity.com/openid/login&openid.claimed_id=https://steamcommunity.com/openid/id/76561198139581989&openid.identity=https://steamcommunity.com/openid/id/76561198139581989&openid.return_to=https://connect-tradeit.com/auth/steam/return?sendTo=https://tradeit.gg/api/v2/steam/login&openid.response_nonce=2023-03-27T12:38:05ZmB7BQaG93vwWQaM10Mn7L7uFHCI=&openid.assoc_handle=1234567890&openid.signed=signed,op_endpoint,claimed_id,identity,return_to,response_nonce,assoc_handle&openid.sig=2eXPDO3x0UV5OpQX0NAaHgkv8u0=', headers=headers)
    #session.get('https://tradeit.gg/api/v2/steam/login?id=76561198139581989&ihash=6c620f1d-7af0-4cee-a5ac-89e95ed410aa&shash=ef291700-606d-4426-a198-3eb89b99dc4c', headers=login_header)
    print(session.get('https://tradeit.gg/api/v2/user/get-intercom-hash',headers=headers).content)

# user_items()

# user_items()


parse_cinv()
