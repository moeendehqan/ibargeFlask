import pymongo
import requests
import random
import datetime
import json
from ast import literal_eval
from Api import CheckUserForApi
client = pymongo.MongoClient()
db = client['barge2']

TokenPayPing = 'OLN--szPEmiOm0-3bvMstEU8hhpiZqsW3ORyvDzYhPE'

payDic = {'pay1':25000,'pay2':42500,'pay3':56250,'pay6':90000,'pay12':150000}

def CreatePay(data):
    check = CheckUserForApi(data['pua'])
    if check['replay'] == False: return check
    phone = check['user']['user']['phone']
    amount = payDic[data['pay']]
    dic = {'amount':amount,'payerIdentity':phone,'clientRefId':str(random.randint(1000000,9999999)),'dateTime':datetime.datetime.now()}
    headers = {'Content-Type': 'application/json','Authorization': f'Bearer {TokenPayPing}'}
    data = json.dumps({'amount':1000,'payerIdentity':phone,'returnURL':r'localhost:3000/paid','clientRefId':dic['clientRefId']})
    response = requests.post(url='https://api.payping.ir/v2/pay',headers=headers,data=data)
    if response.status_code == 200:
        responseCode = literal_eval(response.text)['code']
        dic['responseCode'] = responseCode
        db['paymentsMade'].insert_one(dic)
        return {'replay':True,'responseCode':responseCode}
    return {'replay':False,'msg':'خطا لطفا مجدد امتحان کنید یا با پشتیبانی تماس بگیرید'}



def Check(data):
    check = CheckUserForApi(data['pua'])
    if check['replay'] == False: return check
    print(data)
    return {'replay':True}