import pymongo
import pandas as pd
from Login import getUserByPUA
import cv2  
import numpy as np
import random
import base64
import crypto
import string
from Api import getHistoriByPhone

client = pymongo.MongoClient()
db = client['barge2']




def getMenu():
    pages = db['page'].find({},{'_id':0})
    pages = [x for x in pages]
    menu = {}
    for i in pages:
        for j in i['category']:
            row = i.copy()
            del row['category']
            if j in menu:
                menu[j] = menu[j] + [row]
            else:
                menu[j] = [row]
    return menu

def getHomeMenu():
    pages = pd.DataFrame(db['page'].find({},{'_id':0}))
    pages = pages.sort_values(by=['sort'])
    pages = pages[['title','url','caption']]
    pages = pages.to_dict('records')
    return pages


def getCaptcha():
    font = cv2.FONT_HERSHEY_COMPLEX
    captcha = np.zeros((50,250,3), np.uint8)
    captcha[:] = (11,208,251)
    font= cv2.FONT_HERSHEY_SIMPLEX
    texcode = ''
    listCharector =  string.digits
    for i in range(1,5):
        bottomLeftCornerOfText = (random.randint(35,45)*i,35+(random.randint(-8,8)))
        fontScale= random.randint(7,15)/10
        fontColor= (random.randint(0,250),random.randint(0,250),random.randint(0,250))
        thickness= random.randint(1,4)
        lineType= 1
        text = str(listCharector[random.randint(0,len(listCharector)-1)])
        texcode = texcode+(text)
        cv2.putText(captcha,text,bottomLeftCornerOfText,font,fontScale,fontColor,thickness,lineType)
        if random.randint(0,2)>0:
            pt1 = (random.randint(0,250),random.randint(0,50))
            pt2 = (random.randint(0,250),random.randint(0,50))
            lineColor = (random.randint(0,150),random.randint(0,150),random.randint(0,150))
            cv2.line(captcha,pt1,pt2,lineColor,1)
    stringImg = base64.b64encode(cv2.imencode('.jpg', captcha)[1]).decode()
    return {'captchaCode':crypto.encrypt(texcode),'captchaImg':stringImg}






def getHistori_imageToText(data):
    user = getUserByPUA(data['pua'])
    if user['replay']==False:return user
    histori = getHistoriByPhone(user['user']['phone'],'imagetotext',5)
    return {'replay':True,'histori':histori}

def getHistori_pdfToWord(data):
    user = getUserByPUA(data['pua'])
    if user['replay']==False:return user
    histori = getHistoriByPhone(user['user']['phone'],'pdftoword',5)
    return {'replay':True,'histori':histori}



def getHistori_compressimage(data):
    user = getUserByPUA(data['pua'])
    if user['replay']==False:return user
    histori = getHistoriByPhone(user['user']['phone'],'compressimage',5)
    return {'replay':True,'histori':histori}

def getHistori_compresspdf(data):
    user = getUserByPUA(data['pua'])
    if user['replay']==False:return user
    histori = getHistoriByPhone(user['user']['phone'],'compresspdf',5)
    return {'replay':True,'histori':histori}

def getHistori_mergepdf(data):
    user = getUserByPUA(data['pua'])
    if user['replay']==False:return user
    histori = getHistoriByPhone(user['user']['phone'],'mergepdf',5)
    return {'replay':True,'histori':histori}

def getHistori_extractColors(data):
    user = getUserByPUA(data['pua'])
    if user['replay']==False:return user
    histori = getHistoriByPhone(user['user']['phone'],'extractcolors',5)
    return {'replay':True,'histori':histori}


def getHistori_removebg(data):
    user = getUserByPUA(data['pua'])
    if user['replay']==False:return user
    histori = getHistoriByPhone(user['user']['phone'],'removebg',5)
    return {'replay':True,'histori':histori}