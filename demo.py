import os
import time
import random
import cv2
from PIL import Image
import pyautogui

codes = ['PrimalClash', 'PhantomForces', 'FuriousFists', 'FlashFire', 'PlasmaFreeze', 'PlasmaBlast', 'PlasmaStorm', 'BoundariesCrossed', 'DragonsExalted', 'DarkExplorers', 'Mewtwo2012']
screenPath = './screen/demo.png'

im = pyautogui.screenshot()
screenSize = pyautogui.size()

dip = int(im.size[0] / screenSize.width)

codeImg = Image.open('./tarImg/code-a.png')
btnImg = Image.open('./tarImg/btn-a.png')

posCode = pyautogui.locateCenterOnScreen(codeImg)
posBtn = pyautogui.locateCenterOnScreen(btnImg)

codeLength = len(codes)
index = 0
wait = False

def run(index):
  errTimes = 0
  if posCode != None:
    pyautogui.click(posCode.x / dip, posCode.y / dip, clicks = 2)
    pyautogui.typewrite(codes[index])
    time.sleep(1)
    if posBtn != None:
      pyautogui.click(posBtn.x / dip, posBtn.y / dip)
      print('submit:', index)
      wait = True
      while wait:
        if errTimes > 20:
          wait = False
        else:
          time.sleep(2)
          if pyautogui.locateCenterOnScreen(codeImg) != None:
            index += 1
            if index >= codeLength:
              wait = False
            else:
              run(index)
          else: 
            print('wait:', errTimes)
            errTimes += 1

run(index)
