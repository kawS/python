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
      item['type'] = 'Trainers'
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
def setDetList(typename, stype):
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
          if 'extraInformation' in v:
            del v['extraInformation']
          del v['id']
          del v['url']
          v['series'] = stype
          listNew.append(v)
  jsonTar = json.dumps(listNew, indent = 2, ensure_ascii = False)
  with open('./json/' + typename + '.json', 'w', encoding = 'utf-8') as t:
    t.write(jsonTar)

# setDetList('SV4a', 'SV4.5')

# set 3:
def setEnImg(typename, sname):
  index = 1
  listNew = []
  with open('./lastJson/' + typename + '.json', 'r', encoding = 'utf-8') as f:
    list = f.read()
  jObj = json.loads(list)
  for jtxt in jObj:
    pindex = str(index).zfill(3)
    jtxt['enImgUrl'] = 'https://limitlesstcg.nyc3.digitaloceanspaces.com/tpci/' + sname + '/' + sname + '_' + pindex + '_R_EN.png'
    # jtxt['enImgUrl'] = 'https://tcg.pokemon.com/assets/img/sv-expansions/' + sname + '/cards/en-us/' + sfile + '_' + str(index) + '-2x.jpg'
    # jtxt['enImgUrl'] = 'https://assets.pokemon.com/assets/cms2/img/cards/web/CEL/CEL_EN_' + str(index) + '.png'
    jtxt['cardNo'] = str(index)
    if index > 91:
      jtxt['isHide'] = 'true'
    listNew.append(jtxt)
    index += 1
  jsonTar = json.dumps(listNew, indent = 2, ensure_ascii = False)
  with open('./lastJson/' + typename + '.json', 'w', encoding = 'utf-8') as t:
    t.write(jsonTar)

# setEnImg('SV4_5', 'PAF')

# set 2:
def wrIdNameAIMG(fname, elist, picindex):
  with open('./lastJson/' + fname + '.json', 'r', encoding = 'utf-8') as f:
    _list = f.read()
  jObj = json.loads(_list)
  list = []
  index = 0
  with open('./enInfo/' + elist, 'r', encoding = 'utf-8') as fs:
    _l = fs.read()
    item = json.loads(_l)
  for jtxt in jObj:
    jtxt['ename'] = item[index]['ename']
    jtxt['enImgUrl'] = item[index]['enImgUrl']
    jtxt['cardNo'] = item[index]['cardNo']
    if index > picindex:
      jtxt['imgUrl'] = item[index]['enImgUrl']
      jtxt['isHide'] = 'true'
    index += 1
  jsonTar = json.dumps(jObj, indent = 2, ensure_ascii = False)
  with open('./lastJson/' + fname + '.json', 'w', encoding = 'utf-8') as w:
    w.write(jsonTar)
      
# wrIdNameAIMG('SV6', 'sv6.json', 166)

# 索引
# set 4:
def setSeries(pfile):
  file = './lastJson/' + pfile + '.json'
  with open(file, 'r', encoding = 'utf-8') as f:
    tempData = f.read()
  list = json.loads(tempData)
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

# setSeries('SV6')

# 合并索引
flist = ['SV6', 'SV5', 'SV4_5', 'SV4', 'SV3_5', 'SV3', 'SV2', 'SV1']
# flist = ['SS12_5', 'SS12', 'SS11', 'SS10_5', 'SS10', 'SS9']
arr = []
for item in flist:
  with open('./lastJson/' + item + '-series.json', 'r', encoding = 'utf-8') as f:
    temp = f.read()
  j = json.loads(temp)
  arr = arr + j
with open('./lastJson/SV-series.json', 'w', encoding = 'utf-8') as w:
  w.write(json.dumps(arr, separators = (',', ':'), ensure_ascii = False))



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