import os
import json

def mixJson():
  list = []
  path = './json/SV2D'
  for file in os.listdir(path):
    with open(path + '/' + file, 'r', encoding = 'utf-8') as f:
      fileCons = f.read()
    cons = json.loads(fileCons)
    list.append(cons)
  jsonTxt = json.dumps(list, indent = 2, ensure_ascii = False)
  with open('./json/SV2D.json', 'w', encoding = 'utf-8') as f:
    f.write(jsonTxt)

mixJson()