import requests
import json

def parcer(gameId:int = 730,
           min_price:int = 0,
           max_price:int = 10000000,
           sort:str = 'Popularity',
           limit: int = 1000000):
    data = {}

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/111.0.0.0 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7 '
    }

    response = requests.get(f'https://tradeit.gg/api/v2/inventory/data?gameId={str(gameId)}&limit={str(limit)}&sortType={sort}&searchValue=&minPrice={str(min_price)}&maxPrice={str(max_price)}&minFloat=0&maxFloat=1&showTradeLock=true&colors=&showUserListing=true&fresh=false', headers=headers).json()
    with open('data.json', 'w') as f:
        for i in response['items']:
            try:
                id = i['id']
                _ = {'Name': i['name'], 'ID': id,
                        'Condition' : i['steamTags'][5],
                        'Type': i['steamTags'][0],
                        'Price': i['price']/100,
                        'Count': response['counts'][str(id)]}
                data.update(_)
                json.dump(data, f)
            except KeyError:
                pass
        


parcer()