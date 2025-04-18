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
  with open('./json/' + typename + '1.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

# mixJson()

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
      item['type'] = 'Trainer'
  # print(cons)
  jsonTxt = json.dumps(cons, indent = 2, ensure_ascii = False)
  with open('./json/demo.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

# setAttr()

def toZhCn(pfile):
  converter = OpenCC('t2s')
  with open('./lastJson/' + pfile + '.json', 'r', encoding = 'utf-8') as f:
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
  with open('./lastJson/' + pfile + '-zh.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

# toZhCn('SV1')

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

# set 1:
def setDetList(typename, stype, series):
  listNew = []
  with open('./json/' + typename + '.json', 'r', encoding = 'utf-8') as f:
    list = f.read()
  jObj = json.loads(list)
  for jtxt in jObj:
    id = jtxt['id']
    with open('./json/' + typename + '/' + stype + '-' + id + '.json', 'r', encoding = 'utf-8') as ff:
      v = json.loads(ff.read())
      if 'extraInformation' in v:
        del v['extraInformation']
      del v['id']
      del v['url']
      v['series'] = series
      listNew.append(v)
  jsonTar = json.dumps(listNew, indent = 2, ensure_ascii = False)
  with open('./json/' + typename + '.json', 'w', encoding = 'utf-8') as t:
    t.write(jsonTar)

# setDetList('SV9', 'SV9', 'SV9')

# set 2:
# full mode
# let items = document.querySelectorAll('.card-page-main');
# let arr = [], index = 0;
# for(let i=0;i<items.length;i++){let item = items[i];let tp = '';if(/Supporter/.test(item.querySelector('.card-text-type').innerHTML)){tp = 'Supporter'};
# if(/Stadium/.test(item.querySelector('.card-text-type').innerHTML)){tp = 'Stadium'};
# if(/Item/.test(item.querySelector('.card-text-type').innerHTML)){tp = 'Item'};
# if(/Tool/.test(item.querySelector('.card-text-type').innerHTML)){tp = 'Tool'};arr.push({ename: item.querySelector('.card-text-name a').innerHTML, enImgUrl: item.querySelector('.card').getAttribute('src'), cardNo: `${index + 1}`, isHide: false, pmRule: / ex/.test(item.querySelector('.card-text-name a').innerHTML) ? 'EX' : '', pmSpType: /Tera/.test(item.querySelector('.card-text-ability-info')?.innerHTML) ? 'TERA' : '', spType: '', typeTra: tp});index++}
# JSON.stringify(arr)
def wrIdNameAIMG(fname, elist, picindex):
  with open('./json/' + fname + '.json', 'r', encoding = 'utf-8') as f:
    _list = f.read()
  jObj = json.loads(_list)
  # list = []
  index = 0
  if elist != '':
    with open('./enInfo/' + elist, 'r', encoding = 'utf-8') as fs:
      _l = fs.read()
      item = json.loads(_l)
    # for jtxt in jObj['result']:
    for jtxt in jObj:
      jtxt['ename'] = item['result'][index]['ename']
      jtxt['enImgUrl'] = item['result'][index]['enImgUrl']
      jtxt['cardNo'] = int(item['result'][index]['cardNo'])
      jtxt['isHide'] = item['result'][index]['isHide']
      jtxt['pmRule'] = item['result'][index]['pmRule']
      jtxt['pmSpType'] = item['result'][index]['pmSpType']
      jtxt['spType'] = item['result'][index]['spType']
      jtxt['typeTra'] = item['result'][index]['typeTra']
      if index > picindex:
        jtxt['imgUrl'] = item['result'][index]['enImgUrl']
        jtxt['isHide'] = 'true'
      index += 1
  else:
    for jtxt in jObj:
      index += 1
      jtxt['ename'] = ''
      jtxt['enImgUrl'] = ''
      jtxt['cardNo'] = int(index)
      jtxt['isHide'] = 'false'
      jtxt['pmRule'] = ''
      jtxt['pmSpType'] = ''
      jtxt['spType'] = ''
      jtxt['typeTra'] = ''
  jsonTar = json.dumps(jObj, indent = 2, ensure_ascii = False)
  with open('./json/' + fname + '.json', 'w', encoding = 'utf-8') as w:
    w.write(jsonTar)
      
wrIdNameAIMG('SV9', 'SV9.json', 160)

# 索引
# set 3:
def setSeries(pfile):
  file = './lastJson/' + pfile + '.json'
  with open(file, 'r', encoding = 'utf-8') as f:
    tempData = f.read()
  list = json.loads(tempData)
  list = list['result']
  arr = []
  for item in list:
    # print(item)
    arr.append({
      'name': item['cardName'],
      'ename': item['ename'],
      # 'type': item['type'],
      'series': pfile
    })
  # print(arr)
  with open('./lastJson/' + pfile + '-series.json', 'w', encoding = 'utf-8') as w:
    w.write(json.dumps(arr, separators = (',', ':'), ensure_ascii = False))
    # w.write(json.dumps(arr, indent = 2, ensure_ascii = False))

# setSeries('SV7')

# 合并索引
flist = ['SV7', 'SV6_5', 'SV6', 'SV5', 'SV4_5', 'SV4', 'SV3_5', 'SV3', 'SV2', 'SV1']
# flist = ['SS12_5', 'SS12', 'SS11', 'SS10_5', 'SS10', 'SS9']
# arr = []
# for item in flist:
#   with open('./lastJson/' + item + '-series.json', 'r', encoding = 'utf-8') as f:
#     temp = f.read()
#   j = json.loads(temp)
#   arr = arr + j
# with open('./lastJson/SV-series.json', 'w', encoding = 'utf-8') as w:
#   w.write(json.dumps(arr, separators = (',', ':'), ensure_ascii = False))



# tfile = 'SS5'
# with open('./lastJson/' + tfile + '.json', 'r', encoding = 'utf-8') as f:
#   temp = f.read()
# j = json.loads(temp)
# with open('./BST.json', 'r', encoding = 'utf-8') as fi:
#   tempimg = fi.read()
# img = json.loads(tempimg)
# arr = []
# for i in range(len(j)):
#   j[i]['enImgUrl'] = img[i]

# for item in j:
#   if 'extraInformation' in item:
#     del item['extraInformation']
#   if type(item['cardNo']) == int:
#     item['cardNo'] = str(item['cardNo'])

  # item['isHide'] = 'true'
  # item['imgUrl'] = item['enImgUrl']
  # if type(item['cardNo']) == int:
    # item['cardNo'] = str(item['cardNo'])
  # if 'id' in item:
  #   del item['id']
  # if 'url' in item:
  #   del item['url']
  # if 'extraInformation' in item:
    # del item['extraInformation']
  # if 'artList' in item:
    # del item['artList']
  # if '|' in item['cardNo']:
    # tmp = item['cardNo'].split('|')
    # del tmp[0]
    # item['cardNo'] = '|'.join(tmp)

    # srtu = 'https://tcg.pokemon.com/assets/img/expansions/battle-styles/cards/en-us/SWSH05_EN_' + item['cardNo'] + '-2x.png'
    # item['imgUrl'] = srtu
    # item['enImgUrl'] = srtu
  # arr.append(item)
# print(len(arr))
# with open('./lastJson/' + tfile + '.json', 'w', encoding = 'utf-8') as w:
#   w.write(json.dumps(j, indent = 2, ensure_ascii = False))
  # w.write(json.dumps(arr, indent = 2, ensure_ascii = False))