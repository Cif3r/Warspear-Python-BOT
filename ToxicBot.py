
from asyncio import sleep
from select import select
from sqlite3 import Time
from turtle import delay
import cv2 as cv
import numpy as np
import pyautogui as au
from PIL import ImageGrab
import time
import keyboard

#Metodo de deteccion
method = cv.TM_CCOEFF_NORMED

#Variables globales control de flujo e inicializ221133|acion.
enemySelect = False
attack = False
NumKills = 0

TemplateEnemy = [  './imgs/IMGseleccion/imS0.png', './imgs/IMGseleccion/imS1.png',
                    './imgs/IMGseleccion/imS2.png', './imgs/IMGseleccion/imS3.png', ]


TemplateRecoger = [  './imgs/IMGRecoger/CaidaA.png']
TemplateFaro = './imgs/IMGControl/Faro.png'

SenseNPC = 0.86
SeseRecoger = 0.83
recogido = False
def DetectEnemy():
    global enemySelect

    while enemySelect != True:
        for n in range(len(TemplateEnemy)):
                    cap_arr = np.array(ImageGrab.grab(bbox=(0,0,600,600)))
                    imgGris = cv.cvtColor(cap_arr, cv.COLOR_BGR2GRAY)

                    template = cv.imread(TemplateEnemy[n],0)
                    w, h =  template.shape[::-1]
                    res = cv.matchTemplate(template,imgGris,method)
                    min_val, max_val, min_loc,max_loc = cv.minMaxLoc(res)
                    top_left = max_loc

                    if np.amax(res) > SenseNPC:
                        au.click((top_left[0] + w )-18,(top_left[1] + h)+60)
                        print("NPC Seleccionado")
                        enemySelect = True
                        
                        time.sleep(3)
                        cap_arr = np.array(ImageGrab.grab(bbox=(0,0,600,600)))
                        imgGris = cv.cvtColor(cap_arr, cv.COLOR_BGR2GRAY)
                        template = cv.imread(TemplateFaro,0)
                        w, h =  template.shape[::-1]
                        res2 = cv.matchTemplate(template,imgGris,method)
                        min_val, max_val, min_loc,max_loc = cv.minMaxLoc(res2)
                        top_left = max_loc

                        if np.amax(res2) > 0.8:
                            print("Desbloqueando mira")
                            au.click((top_left[0] + w ),(top_left[1] + h)-130)
                            au.click((top_left[0] + w )-60,(top_left[1] + h)-90)
                            
                        break
                    cap_arr = 0

def collect():
    global recogido 
    for n in range(len(TemplateRecoger)):
        ca = np.array(ImageGrab.grab(bbox=(0,0,600,600)))
        imgGris = cv.cvtColor(ca, cv.COLOR_BGR2GRAY)

        template = cv.imread(TemplateRecoger[n],0)
        w, h =  template.shape[::-1]
        rec = cv.matchTemplate(template,imgGris,method)
        min_val, max_val, min_loc,max_loc = cv.minMaxLoc(rec)
        top_left = max_loc

        if np.amax(rec) > SeseRecoger:
            if n == 0: 
                recogido = True
                time.sleep(1.4)
                au.click((top_left[0] + w )-16,(top_left[1] + h)+30)
                time.sleep(2)
                reinciar()
                break
            break

    

def AttackEnemy():
    global recogido
   #https://pythonbros.com/controlar-el-teclado-con-python/
    if recogido == False:

        keyboard.send("2")
        keyboard.send("2")

        keyboard.send("3")
        keyboard.send("3")

        keyboard.send("1")
        keyboard.send("1")

        keyboard.send("4")
        keyboard.send("4")

        #Lo repito para que no quede 123seleccionada la habilidad y no pueda recoger el botin

    #intento recoger

def reinciar():
    global enemySelect
    global recogido
    global NumKills
    keyboard.send("enter")
    print("Punto de inicio")
    NumKills += 1
    print("Conteo", NumKills)
    enemySelect = False
    recogido = False
    time.sleep(1)
    cap_1 = np.array(ImageGrab.grab(bbox=(0,0,600,600)))
    imgGris = cv.cvtColor(cap_1, cv.COLOR_BGR2GRAY)
    template = cv.imread(TemplateFaro,0)
    w, h =  template.shape[::-1]
    res3 = cv.matchTemplate(template,imgGris,method)
    min_val, max_val, min_loc,max_loc = cv.minMaxLoc(res3)
    top_left = max_loc
    
    if np.amax(res3) > 0.8:
        time.sleep(2)
        au.click((top_left[0] + w ),(top_left[1] + h)-60)


    time.sleep(1)
    keyboard.send("5")


while True:
    DetectEnemy()
    AttackEnemy()
    collect()
    if cv.waitKey(1) == 27:
       cv.destroyAllWindows()
       break
