import os
import json
import re
from opencc import OpenCC

def mixJson(typename):
  lists = []
  path = './json/' + typename
  for file in os.listdir(path):
    if file == '.DS_Store':
      continue
    with open(path + '/' + file, 'r', encoding = 'utf-8') as f:
      fileCons = f.read()
    cons = json.loads(fileCons)
    lists.append(cons)
    # lists = lists + cons
  jsonTxt = json.dumps(lists, indent = 2, ensure_ascii = False)
  with open('./json/' + typename + '.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

# mixJson('S10b')

def setAttr():
  with open('./json/demo.json', 'r', encoding = 'utf-8') as f:
    file = f.read()
  cons = json.loads(file)
  for item in cons:
    if 'extraInformation' in item:
      item['type'] = 'Pokemon'
    elif re.search(r'能量', item['cardName']) != None:
      item['type'] = 'Energy'
    else:
      item['type'] = 'Trainers'
  # print(cons)
  jsonTxt = json.dumps(cons, indent = 2, ensure_ascii = False)
  with open('./json/demo.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

# setAttr()

def toZhCn():
  converter = OpenCC('t2s')
  with open('./json/temp.json', 'r', encoding = 'utf-8') as f:
    file = f.read()
  cons = json.loads(file)
  for item in cons:
    item['cardName'] = converter.convert(item['cardName'])
    for s in item['skillList']:
      s['name'] = converter.convert(s['name'])
      s['effect'] = converter.convert(s['effect'])
    if 'extraInformation' in item:
      for index in range(len(item['extraInformation'])):
        item['extraInformation'][index] = converter.convert(item['extraInformation'][index])
        # print(s)
  # print(cons[0])
  jsonTxt = json.dumps(cons, indent = 2, ensure_ascii = False)
  with open('./json/temp.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

# toZhCn()

def setAttrType():
  type = {
    '1': {
      'name': '草',
      'value': 'Grass',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Grass.png'
    },
    '2': {
      'name': '火',
      'value': 'Fire',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Fire.png'
    },
    '3': {
      'name': '水',
      'value': 'Water',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Water.png'
    },
    '4': {
      'name': '雷',
      'value': 'Lightning',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Lightning.png'
    },
    '5': {
      'name': '超',
      'value': 'Psychic',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Psychic.png'
    },
    '6': {
      'name': '斗',
      'value': 'Fighting',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Fighting.png'
    },
    '7': {
      'name': '恶',
      'value': 'Darkness',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Darkness.png'
    },
    '8': {
      'name': '钢',
      'value': 'Metal',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Metal.png'
    },
    '9': {
      'name': '妖精',
      'value': 'Fairy',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Fairy.png'
    },
    '10': {
      'name': '龙',
      'value': 'Dragon',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Dragon.png'
    },
    '11': {
      'name': '无',
      'value': 'Colorless',
      'imgUrl': 'https://asia.pokemon-card.com/various_images/energy/Colorless.png'
    }
  }
  for file in os.listdir('./json/type'):
    with open('./json/type/' + file, 'r', encoding = 'utf-8') as f:
      jtext = f.read()
    cons = json.loads(jtext)
    if len(cons) > 0:
      index = str(int(file.split('.')[0]))
      for item in cons:
        # print(type[index]['name'])
        item['typeEnergy'] = type[index]['value']
      jsonTxt = json.dumps(cons, indent = 2, ensure_ascii = False)
      with open('./json/type/' + file, 'w', encoding = 'utf-8') as f:
        f.write(jsonTxt)

# setAttrType()


def setDet(typename):
  listNew = []
  with open('./json/' + typename + '.json', 'r', encoding = 'utf-8') as f:
    list = f.read()
  jObj = json.loads(list)
  for jtxt in jObj:
    id = jtxt['id']
    for file in os.listdir('./json/' + typename):
      with open('./json/' + typename + '/' + file, 'r', encoding = 'utf-8') as ff:
        if file == '.DS_Store':
          continue
        v = json.loads(ff.read())
        if v['id'] == id:
          listNew.append(v)
  jsonTar = json.dumps(listNew, indent = 2, ensure_ascii = False)
  with open('./json/' + typename + '.json', 'w', encoding = 'utf-8') as t:
    t.write(jsonTar)

setDet('S11')
