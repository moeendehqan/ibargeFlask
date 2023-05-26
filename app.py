from flask import Flask, request
import json
import warnings
from flask_cors import CORS
import winreg as reg
import pymongo
from waitress import serve

client = pymongo.MongoClient()
db = client['barge']


def addToReg():
    key = reg.OpenKey(reg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" ,0 , reg.KEY_ALL_ACCESS)
    reg.SetValueEx(key ,"ibargeFlask" , 0 , reg.REG_SZ , __file__)
    reg.CloseKey(key)

addToReg()
warnings.filterwarnings("ignore")
app = Flask(__name__)
CORS(app)





if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=8080)
    app.run(host='0.0.0.0', debug=True)