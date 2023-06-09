import crypto
import random
import datetime
from melipayamak import Api
import pymongo
client = pymongo.MongoClient()
db = client['barge2']


sms = {'url':'http://api.payamak-panel.com/post/Send.asmx','username':'9011010959','password':'@8F20'}
api = Api('9011010959','@8F20')
sms_rest = api.sms()


def applyPhone(data):
    captchaCrypto = crypto.decrypt(data['captchaCrypto'])
    if captchaCrypto != data['captcha']: return {'replay':False,'msg':'کد کپچا صحیح نیست'}
    codeSms = random.randint(10000, 99999)
    date = datetime.datetime.now()
    sms_rest.send_by_base_number(str(codeSms), data['phone'], '130566')
    db['code'].insert_one({'phone':data['phone'],'codeSms':codeSms,'date':date})
    print(codeSms)
    return {'replay':True}


def applyCode(data):
    codeSms = db['code'].find({'phone':data['phone']}).sort('date',pymongo.DESCENDING).limit(1)
    if codeSms == None: return {'replay':False,'msg':'کد اشتباه است'}
    codeSms = [x for x in codeSms][0]['codeSms']
    if str(codeSms) != str(data['code']): return {'replay':False,'msg':'کد اشتباه است'}
    cookie = crypto.encrypt(data['phone'])
    user = db['user'].find_one({'phone':data['phone']})
    if user == None:
        dic = {'phone':data['phone'],'register':datetime.datetime.now(), 'credit': datetime.datetime.now() + datetime.timedelta(days=7),'type':'حقیقی'}
        db['user'].insert_one(dic)
    return {'replay':True,'cookie':cookie}



def loginByPUA(data):
    try:
        pua = crypto.decrypt(data['pua'])
    except:
        return {'replay':False}
    user = db['user'].find_one({'phone':pua})
    if user == None:
        return {'replay':False}
    return {'replay':True}


def getUserByPUA(data):
    try:
        pua = crypto.decrypt(data)
    except:
        return {'replay':False}
    user = db['user'].find_one({'phone':pua},{'_id':0})
    if user == None:
        return {'replay':False}
    user['creditDay'] = max((user['credit'] - datetime.datetime.now()).days,0)
    if user['creditDay']>21:user['hearts'] = [True,True,True,True]
    elif user['creditDay']>14:user['hearts'] = [True,True,True,False]
    elif user['creditDay']>7:user['hearts'] = [True,True,False,False]
    elif user['creditDay']>0:user['hearts'] = [True,False,False,False]
    else:user['hearts'] = [False,False,False,False]
    return {'replay':True,'user':user}
