from bs4 import BeautifulSoup
import requests
import urllib3
import json
import re
import time
import os
from opencc import OpenCC

_dict = [
  { 'series': 'FB01', 'url': 'https://dbs-cardgame.com/fw/en/cardlist/?search=true&category%5B%5D=583001' },
  { 'series': 'FS01', 'url': 'https://dbs-cardgame.com/fw/en/cardlist/?search=true&q=&category%5B%5D=583101'},
  { 'series': 'FS02', 'url': 'https://dbs-cardgame.com/fw/en/cardlist/?search=true&q=&category%5B%5D=583102'},
  { 'series': 'FS03', 'url': 'https://dbs-cardgame.com/fw/en/cardlist/?search=true&q=&category%5B%5D=583103'},
  { 'series': 'FS04', 'url': 'https://dbs-cardgame.com/fw/en/cardlist/?search=true&q=&category%5B%5D=583104'},
  { 'series': 'FP', 'url': 'https://dbs-cardgame.com/fw/en/cardlist/?search=true&q=&category%5B%5D=583901'}
]

def getList():
  for dictItem in _dict:
    req = requests.get(dictItem['url'])
    if req.status_code == 200:
      soup = BeautifulSoup(req.text, 'html.parser')
      itemList = soup.find_all('li', class_='cardItem')
      result = []
      for item in itemList:
        src = 'https://dbs-cardgame.com/fw/en/cardlist/' + item.find('a')['data-src']
        result.append({ 'url': src })
      json_ = json.dumps(result, indent = 2, ensure_ascii = False)
      with open('./dbs/' + dictItem['series'] + '.txt', 'w', encoding = 'utf-8') as f:
        f.write(json_)

def getDet(series, cindex):
  with open('./dbs/' + series + '.txt', 'r', encoding = 'utf-8') as f:
    strList = f.read()
  rJson = json.loads(strList)
  itemCount = len(rJson)
  index = 1
  result = []
  path = 'https://dbs-cardgame.com/fw'
  for item in rJson:
    if index <= cindex - 10:
      index += 1
      continue
    if index > cindex:
      break
    requests.DEFAULT_RETRIES = 10
    s = requests.session()
    s.keep_alive = False
    urllib3.disable_warnings()
    print(str(index) + ' / ' + str(itemCount))
    req = requests.get(item['url'])
    req.close()
    time.sleep(5)
    if req.status_code == 200:
      cardDet = {}
      soup = BeautifulSoup(req.text, 'html.parser')
      cardDet['series'] = series
      cardDet['no'] = soup.find('div', class_='cardNo').get_text()
      cardDet['rarity'] = soup.find('div', class_='rarity').get_text()
      nameList = []
      nameDom = soup.find_all('h1', class_='cardName')
      for n in nameDom:
        nameList.append(n.get_text())
      isLeader = True if len(nameList) > 1 else False
      cardDet['name'] = nameList
      imgList = []
      if isLeader == True:
        imgDom = soup.find_all('div', class_='cardImageImg')
      else:
        imgDom = soup.find_all('div', class_='cardImage')
      for n in imgDom:
        imgList.append(n.find('img')['src'].replace('../..', path))
      cardDet['img'] = imgList
      cardData = soup.find_all('div', class_='cardDataRow')
      for i in range(len(cardData)):
        cell = cardData[i].find_all('div', class_='cardDataCell')
        if i == 0:
          cardDet['type'] = cell[0].find('div', class_='data').get_text()
          cardDet['color'] = cell[1].find('div', class_='colValue').get_text()
        if i == 1:
            cardDet['cost'] = cell[0].find('div', class_='data').get_text()
            cardDet['specifiedCost'] = cell[1].find('div', class_='data').get_text().replace('\n', '').replace('\r', '').replace(' ', '')
        if i == 2:
          powerList = []
          powerDom = cell[0].find_all('div', class_='data')
          for n in powerDom:
            powerList.append(n.get_text())
          cardDet['power'] = powerList
          cardDet['comboPower'] = cell[1].find('div', class_='data').get_text()
        if i == 3:
          cardDet['features'] = cell[0].find('div', class_='data').get_text().replace('\n', '').replace('\r', '').replace(' ', '')
        if i == 4:
          effectList = []
          effectDom = cell[0].find_all('div', class_='data')
          for n in effectDom:
            temp = n.get_text('|', strip = True).split('|')
            effectList.append(temp)
          cardDet['effect'] = effectList
        if i == 5:
          cardDet['productName'] = cell[0].find('div', class_='data').get_text()
      if isLeader == True:
        cardDet['isSwitch'] = '1'
      else:
        cardDet['isSwitch'] = '-1'
      cardDet['isShow'] = '1'
      result.append(cardDet)
      index += 1
  s = json.dumps(result, indent = 2, ensure_ascii = False)
  with open('./dbs/' + series + '-' + str(cindex) + '.json', 'w', encoding = 'utf-8') as f:
    f.write(s)
      
# getList()
# getDet('FP', 60)
