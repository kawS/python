from bs4 import BeautifulSoup
import requests
import urllib3
import json
import re
import time
import os
from opencc import OpenCC

def getList(name):
  tarUrl = 'https://www.dbs-cardgame.com/fw/en/cardlist/?search=true&category%5B0%5D=583002'
  req = requests.get(tarUrl)
  if req.status_code == 200:
    soup = BeautifulSoup(req.text, 'html.parser')
    itemList = soup.find_all('li', class_='cardItem')
    result = []
    for item in itemList:
      src = 'https://www.dbs-cardgame.com/fw/en/cardlist/' + item.find('a')['data-src']
      result.append({'src': src})
    json_ = json.dumps(result, indent = 2, ensure_ascii = False)
    with open('./dbs/' + name + '.txt', 'w', encoding = 'utf-8') as f:
      f.write(json_)

def getDet(name, cindex, sat = 10):
  with open('./dbs/' + name + '.txt', 'r', encoding = 'utf-8') as f:
    strList = f.read()
  rJson = json.loads(strList)
  itemCount = len(rJson)
  index = 1
  result = []
  for item in rJson:
    if index <= cindex - sat:
      index += 1
      continue
    if index > cindex:
      break
    requests.DEFAULT_RETRIES = 10
    s = requests.session()
    s.keep_alive = False
    urllib3.disable_warnings()
    print(str(index) + ' / ' + str(itemCount))
    req = requests.get(item['src'])
    req.close()
    time.sleep(5)
    if req.status_code == 200:
      cardDet = {}
      soup = BeautifulSoup(req.text, 'html.parser')
      cardDet['series'] = name
      cardDet['no'] = soup.find('div', class_='cardNo').get_text()
      cardDet['rarity'] = soup.find('div', class_="rarity").get_text()
      nameDom = soup.find_all('h1', class_='cardName')
      nameList = []
      for n in nameDom:
        nameList.append(n.get_text())
      isLeader = True if len(nameList) > 1 else False
      imgList = []
      if isLeader == True:
        imgDom = soup.find_all('div', class_='cardImageImg')
        for n in imgDom:
          imgList.append(n.find('img')['src'].replace('../..', 'https://www.dbs-cardgame.com/fw'))
      else:
        imgDom = soup.find('div', class_='cardImage')
        imgList.append(imgDom.find('img')['src'].replace('../..', 'https://www.dbs-cardgame.com/fw'))
      cardDet['name'] = nameList
      cardDet['img'] = imgList
      cardData = soup.find_all('div', class_='cardDataRow')
      d1 = cardData[0].find_all('div', class_='cardDataCell')
      cardDet['type'] = d1[0].find('div', class_='data').get_text()
      cardDet['color'] = d1[1].find('div', class_='data').get_text().replace('\n', '')
      d2 = cardData[1].find_all('div', class_='cardDataCell')
      cardDet['cost'] = d2[0].find('div', class_='data').get_text()
      cardDet['specifiedCost'] = d2[1].find('div', class_='data').get_text().replace('\n', '').replace('\r', '').replace(' ', '')
      d3 = cardData[2].find_all('div', class_='cardDataCell')
      powerList = []
      powerDom = d3[0].find_all('div', class_='data')
      for n in powerDom:
        powerList.append(n.get_text())
      cardDet['power'] = powerList
      cardDet['comboPower'] = d3[1].find('div', class_='data').get_text()
      cardDet['features'] = cardData[3].find('div', class_='data').get_text().replace('\n', '').replace('\r', '').replace(' ', '')
      effectList = []
      effectDom = cardData[4].find_all('div', class_='data')
      for n in effectDom:
        temp = n.get_text('|', strip=True).split('|')
        effectList.append(temp)
      cardDet['effect'] = effectList
      cardDet['productName'] = cardData[5].find('div', class_='data').get_text()
      if isLeader == True:
        cardDet['isSwitch'] = '1'
      else:
        cardDet['isSwitch'] = '-1'
      cardDet['isShow'] = '1'
      result.append(cardDet)
      index += 1
  s = json.dumps(result, indent = 2, ensure_ascii = False)
  with open('./dbs/' + name + '-' + str(cindex) + '-' + str(sat) + '.json', 'w', encoding = 'utf-8') as f:
    f.write(s)
      
# getList('FB02')
# getDet('FB02', 163, 23)

def setSeries(pfile):
  file = './dbs/' + pfile + '.json'
  with open(file, 'r', encoding = 'utf-8') as f:
    tempData = f.read()
  list = json.loads(tempData)
  arr = []
  for item in list:
    # print(item)
    arr.append({
      'name': item['name'][0],
      'series': item['series']
    })
  # print(arr)
  with open('./dbs/sy/' + pfile + '-series.json', 'w', encoding = 'utf-8') as w:
    w.write(json.dumps(arr, separators = (',', ':'), ensure_ascii = False))
    # w.write(json.dumps(arr, indent = 2, ensure_ascii = False))
# setSeries('FB02')
flist = ['FB02', 'FB01', 'FP', 'FS01', 'FS02', 'FS03', 'FS04']
arr = []
for item in flist:
  with open('./dbs/sy/' + item + '-series.json', 'r', encoding = 'utf-8') as f:
    temp = f.read()
  j = json.loads(temp)
  arr = arr + j
with open('./dbs/sy/series.json', 'w', encoding = 'utf-8') as w:
  w.write(json.dumps(arr, separators = (',', ':'), ensure_ascii = False))