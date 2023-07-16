from bs4 import BeautifulSoup
import requests
import json
import re

exReg = re.compile(r'\d+')
typeList = ['SV2D', 'SV2P']

def parse(items):
  for item in items:
    yield {
      'id': exReg.findall(item.a.get('href'))[0],
      'url': item.a.get('href'),
      'imgUrl': item.find('img')['data-original']
    }

def startGet(type, pi):
  pageIndex = pi
  tarUrl = 'https://asia.pokemon-card.com/tw/card-search/list/?sortCondition=&keyword=&cardType=all&regulation=1&pokemonEnergy=&pokemonWeakness=&pokemonResistance=&pokemonMoveEnergy=&hpLowerLimit=none&hpUpperLimit=none&retreatCostLowerLimit=0&retreatCostUpperLimit=none&illustratorName=&expansionCodes=' + type + '&pageNo=' + str(pageIndex)
  req = requests.get(tarUrl)
  if req.status_code == 200:
    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup.select('.resultHeader .resultTotalPages'))
    pageCount = int(exReg.findall(soup.find('div', class_='resultHeader').find('p', class_='resultTotalPages').text)[0])
    itemList = soup.find_all('li', class_='card')
    result = list(parse(itemList))
    s = json.dumps(result, indent = 2, ensure_ascii = False)
    fname = './json/' + type + '-' + str(pageIndex)+ '.json'
    with open(fname, 'w', encoding = 'utf-8') as f:
      f.write(s)
    if pageIndex < pageCount:
      startGet(type, pageIndex + 1)

startGet(typeList[0], 1)