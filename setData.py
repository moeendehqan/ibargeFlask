import pymongo
import datetime


client = pymongo.MongoClient()
db = client['barge2']


def setProfile(data):
    dic = data
    for i in ['credit','creditDay','hearts','register']:
        if i in dic: del dic[i]
    if 'dateBirth' in dic and type(dic['dateBirth']) == int: 
        dic['dateBirth'] = datetime.datetime.fromtimestamp(dic['dateBirth']/1000)

    if dic['type'] == 'حقوقی':del dic['dateBirth']

    db['user'].update_one({'phone':data['phone']},{'$set':dic})

    return {'replay':True}


