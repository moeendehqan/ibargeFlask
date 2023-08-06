import pymongo
from persiantools.jdatetime import JalaliDate
import json
import crypto
from ast import literal_eval
import pandas as pd
client = pymongo.MongoClient()
db = client['barge2']

accounting = {'username':'moeen','password':'Moeen....6168'}

def dateConvert(date):
    print(date)
    if date!='' and date:
        return str(JalaliDate.to_gregorian(date))
    return date

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


def getusers(data):
    Cheack = json.loads(cookie(data))
    print(Cheack)
    if Cheack['reply']:
        df = pd.DataFrame(db['user'].find({},{'_id':0}))
        df = df.fillna('')
        print(df)
        if 'register' in df.columns: df['register'] = df['register'].apply(dateConvert)
        if 'credit' in df.columns: df['credit'] = df['credit'].apply(dateConvert)
        if 'dateBirth' in df.columns: df = df.drop(columns='dateBirth')
        df = df.to_dict('records')
        return json.dumps({'reply':True,'df':df})
    else:
        return cookie(data)
