import pymongo
from persiantools.jdatetime import JalaliDate
import json
import crypto
from ast import literal_eval
client = pymongo.MongoClient()
db = client['barge2']

accounting = {'username':'moeen','password':'Moeen....6168'}

def login(data):
    if data['username'] == accounting['username'] and data['password']==accounting['password']:
        cliadmin = crypto.encrypt(str(accounting))
        return json.dumps({'reply':True,'cliadmin':cliadmin})
    else:
        return json.dumps({'reply':False,'msg':'Internet connection is not established'})


def cookie(data):
    try:
        cliadmin = data['cliadmin']
        cliadmin = str(cliadmin)
        cliadmin = crypto.decrypt(cliadmin)
        cliadmin = literal_eval(cliadmin)
        return login(cliadmin)
    except:
        return json.dumps({'reply':False})
