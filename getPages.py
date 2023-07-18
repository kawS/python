from bs4 import BeautifulSoup
import requests
import json
import re
import time
import os

exReg = re.compile(r'\d+')
# typeList = ['SV2D', 'SV2P', 'SV1a', 'SVC]
typeList = ['SVC']
resultList = []

def parse(items):
  for item in items:
    yield {
      'id': exReg.findall(item.a.get('href'))[0],
      'url': 'https://asia.pokemon-card.com' + item.a.get('href'),
      'imgUrl': item.find('img')['data-original']
    }

def startGet(type, pi):
  global resultList
  pageIndex = pi
  tarUrl = 'https://asia.pokemon-card.com/tw/card-search/list/?sortCondition=&keyword=&cardType=all&regulation=1&pokemonEnergy=&pokemonWeakness=&pokemonResistance=&pokemonMoveEnergy=&hpLowerLimit=none&hpUpperLimit=none&retreatCostLowerLimit=0&retreatCostUpperLimit=none&illustratorName=&expansionCodes=' + type + '&pageNo=' + str(pageIndex)
  req = requests.get(tarUrl)
  if req.status_code == 200:
    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup.select('.resultHeader .resultTotalPages'))
    pageCount = int(exReg.findall(soup.find('div', class_='resultHeader').find('p', class_='resultTotalPages').text)[0])
    itemList = soup.find_all('li', class_='card')
    resultList = resultList + list(parse(itemList))
    if pageIndex < pageCount:
      startGet(type, pageIndex + 1)
    else:
      toJsonFile(resultList, type)

def toJsonFile(data, type, filepath = ''):
  s = json.dumps(data, indent = 2, ensure_ascii = False)
  fname = './json/' + filepath + type + '.json'
  with open(fname, 'w', encoding = 'utf-8') as f:
    f.write(s)

def getSerData():
  for index in range(len(typeList)):
    global resultList
    startGet(typeList[index], 1)

def getSerDet(type):
  with open('./json/' + type + '.json', 'r', encoding = 'utf-8') as f:
    str = f.read()
  rJson = json.loads(str)
  for item in rJson:
    s = requests.session()
    req = requests.get(item['url'], verify = False)
    req.close()
    if req.status_code == 200:
      soup = BeautifulSoup(req.text, 'html.parser')
      cardNameDom = soup.find('li', class_='step active')
      if cardNameDom == None:
        cardName = soup.find('h1', class_='cardDetail').get_text().replace('\n','').replace(' ','')
      else:
        cardName = cardNameDom.find('a').get_text()
      itemType = soup.find('h3', class_='commonHeader').get_text().replace('\n','').replace(' ','')
      skillDom = soup.find_all('div', class_='skill')
      skillList = []
      for dom in skillDom:
        name = dom.find('span', class_='skillName').get_text()
        effect = dom.find('p', class_='skillEffect').get_text()
        if name != '' or (name == '' and (itemType == '物品卡' or itemType == '支援者卡' or itemType == '寶可夢道具' or itemType == '競技場卡' or itemType == '特殊能量卡' or itemType == '基本能量卡')):
          skillList.append({
            'name': name,
            'effect': effect.strip().replace('\n','')
          })
      # if itemType != '物品卡' and itemType != '支援者卡' and itemType != '寶可夢道具' and itemType != '競技場卡' and itemType != '特殊能量卡' and itemType != '基本能量卡':
      if itemType == '招式':
        einfoDom = [
          soup.find('div', class_='extraInformation').find('h3'),
          soup.find('p', class_='size'),
          soup.find('p', class_='discription')
        ]
        extraInformation = [
          '' if einfoDom[0] == None else einfoDom[0].get_text().replace('\n','').replace(' ',''),
          '' if einfoDom[1] == None else einfoDom[1].get_text().replace('\n','').replace(' ',''),
          '' if einfoDom[2] == None else einfoDom[2].get_text().replace('\n','').replace(' ','')
        ]
        item['extraInformation'] = extraInformation
      if itemType == '招式':
        item['type'] = 'Pokemon'
      elif (itemType == '特殊能量卡' or itemType == '基本能量卡'):
        item['type'] = 'Energy'
      else:
        item['type'] = 'Trainers'
      item['cardName'] = cardName
      item['skillList'] = skillList
      toJsonFile(item, type + '-' + item['id'], type + '/')
      print(item['id'])
    time.sleep(20)
  # s = json.dumps(rJson, indent = 2, ensure_ascii = False)
  # with open('./json/' + type + '.json', 'w', encoding = 'utf-8') as f:
  #   f.write(s)

# getSerData()
getSerDet('SVC')


def mixJson():
  list = []
  path = './json/SVC'
  for file in os.listdir(path):
    if file == '.DS_Store':
      continue
    with open(path + '/' + file, 'r', encoding = 'utf-8') as fs:
      fileCons = fs.read()
    cons = json.loads(fileCons)
    list.append(cons)
  jsonTxt = json.dumps(list, indent = 2, ensure_ascii = False)
  with open('./json/SVC.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

# mixJson()
