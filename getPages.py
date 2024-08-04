from bs4 import BeautifulSoup
import requests
import urllib3
import json
import re
import time
import os
from opencc import OpenCC

exReg = re.compile(r'\d+')
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
  print(fname)
  with open(fname, 'w', encoding = 'utf-8') as f:
    f.write(s)

def getSerData():
  for index in range(len(typeList)):
    global resultList
    startGet(typeList[index], 1)

def getSerDet(type):
  index = 0
  converter = OpenCC('t2s')
  with open('./json/' + type + '.json', 'r', encoding = 'utf-8') as f:
    jStr = f.read()
  rJson = json.loads(jStr)
  itemCount = len(rJson)
  for item in rJson:
    requests.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    urllib3.disable_warnings()
    print(item['id'] + ' - start')
    req = requests.get(item['url'])
    req.close()
    time.sleep(20)
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
            'name': converter.convert(name),
            'effect': converter.convert(effect.strip().replace('\n',''))
          })
      # if itemType != '物品卡' and itemType != '支援者卡' and itemType != '寶可夢道具' and itemType != '競技場卡' and itemType != '特殊能量卡' and itemType != '基本能量卡':
      if itemType == '招式':
        einfoDom = [
          soup.find('div', class_='extraInformation').find('h3'),
          soup.find('p', class_='size'),
          soup.find('p', class_='discription')
        ]
        extraInformation = [
          '' if einfoDom[0] == None else converter.convert(einfoDom[0].get_text().replace('\n','').replace(' ','')),
          '' if einfoDom[1] == None else converter.convert(einfoDom[1].get_text().replace('\n','').replace(' ','')),
          '' if einfoDom[2] == None else converter.convert(einfoDom[2].get_text().replace('\n','').replace(' ',''))
        ]
        item['extraInformation'] = extraInformation
        typeDomArr = soup.find('p', class_='mainInfomation').find('img')['src'].split('/')
        typeName = typeDomArr[len(typeDomArr) - 1].split('.')[0]
        item['typeEnergy'] = typeName
      if itemType == '招式':
        item['type'] = 'Pokemon'
      elif (itemType == '特殊能量卡' or itemType == '基本能量卡'):
        item['type'] = 'Energy'
      else:
        item['type'] = 'Trainers'
      item['cardName'] = converter.convert(cardName)
      item['skillList'] = skillList
      # toJsonFile(item, type + '-' + item['id'], type + '/')
      toJsonFile(item, type + '-' + item['id'], '')
      index += 1
      print('(' + str(index) + ' / ' + str(itemCount) + ')' + ' end')
      if index == itemCount:
        print('all over')
  # s = json.dumps(rJson, indent = 2, ensure_ascii = False)
  # with open('./json/' + type + '.json', 'w', encoding = 'utf-8') as f:
  #   f.write(s)

# set 1:
typeList = ['SV7']
# getSerData()
# set 2:
# getSerDet('SV7')
