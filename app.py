from flask import Flask, request, send_file
import json
import warnings
from flask_cors import CORS
import winreg as reg
import pymongo
from waitress import serve
import pay
import getData
import Login
import setData
import Api
client = pymongo.MongoClient()
db = client['barge2']


def addToReg():
    key = reg.OpenKey(reg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" ,0 , reg.KEY_ALL_ACCESS)
    reg.SetValueEx(key ,"ibargeFlask" , 0 , reg.REG_SZ , __file__)
    reg.CloseKey(key)

addToReg()
warnings.filterwarnings("ignore")
app = Flask(__name__)
CORS(app)


@app.route('/getmenu',methods=['POST'])
def getmenu():
    return getData.getMenu()

@app.route('/gethomemenu',methods=['POST'])
def gethomemenu():
    return getData.getHomeMenu()

@app.route('/getcaptcha',methods=['POST'])
def getcaptcha():
    return getData.getCaptcha()

@app.route('/applyphone',methods=['POST'])
def applyphone():
    data = request.get_json()
    return Login.applyPhone(data)

@app.route('/applycode',methods=['POST'])
def applycode():
    data = request.get_json()
    return Login.applyCode(data)

@app.route('/loginbypua',methods=['POST'])
def loginbypua():
    data = request.get_json()
    return Login.loginByPUA(data)

@app.route('/getuserbypua',methods=['POST'])
def getuserbypua():
    data = request.get_json()
    return Login.getUserByPUA(data['pua'])

@app.route('/setprofile',methods=['POST'])
def setprofile():
    data = request.get_json()
    return setData.setProfile(data)

@app.route('/api/imagetotext',methods=['POST'])
def imagetotext():
    file = request.files['file']
    pua = request.form['pua']
    option = request.form['option']
    return Api.imageToText(file,pua,option)

@app.route('/api/pdftoword',methods=['POST'])
def pdftoword():
    file = request.files['file']
    pua = request.form['pua']
    option = request.form['option']
    return Api.pdfToWord(file,pua,option)

@app.route('/api/convertdate',methods=['POST'])
def convertdate():
    data = request.get_json()
    return Api.convertDate(data)

@app.route('/api/loremipsum',methods=['POST'])
def loremipsum():
    data = request.get_json()
    return Api.loremIpsum(data)

@app.route('/api/pdftotext',methods=['POST'])
def pdftotext():
    file = request.files['file']
    pua = request.form['pua']
    option = request.form['option']
    return Api.pdfToText(file,pua,option)

@app.route('/api/compressimage',methods=['POST'])
def compressimage():
    file = request.files['file']
    pua = request.form['pua']
    option = request.form['option']
    return Api.compressimage(file,pua,option)

@app.route('/api/imagefrompdf',methods=['POST'])
def imagefrompdf():
    file = request.files['file']
    pua = request.form['pua']
    return Api.imagefrompdf(file,pua)

@app.route('/api/compresspdf',methods=['POST'])
def compresspdf():
    file = request.files['file']
    pua = request.form['pua']
    return Api.compresspdf(file,pua)

@app.route('/api/mergepdf',methods=['POST'])
def mergepdf():
    file1 = request.files['file1']
    file2 = request.files['file2']
    pua = request.form['pua']
    return Api.mergepdf(file1,file2,pua)

@app.route('/api/extractcolors',methods=['POST'])
def extractColors():
    file = request.files['file']
    pua = request.form['pua']
    option = request.form['option']
    return Api.extractColors(file,option,pua)

@app.route('/api/removebg',methods=['POST'])
def removeBg():
    file = request.files['file']
    pua = request.form['pua']
    return Api.removeBg(file,pua)

@app.route('/gethistori/imagetotext',methods=['POST'])
def getHistori_imageToText():
    data = request.get_json()
    return getData.getHistori_imageToText(data)

@app.route('/gethistori/pdftoword',methods=['POST'])
def getHistori_pdfToWord():
    data = request.get_json()
    return getData.getHistori_pdfToWord(data)

@app.route('/gethistori/compressimage',methods=['POST'])
def getHistori_compressimage():
    data = request.get_json()
    return getData.getHistori_compressimage(data)


@app.route('/gethistori/compresspdf',methods=['POST'])
def getHistori_compresspdf():
    data = request.get_json()
    return getData.getHistori_compresspdf(data)

@app.route('/gethistori/mergepdf',methods=['POST'])
def getHistori_mergepdf():
    data = request.get_json()
    return getData.getHistori_mergepdf(data)

@app.route('/gethistori/extractcolors',methods=['POST'])
def getHistori_extractColors():
    data = request.get_json()
    return getData.getHistori_extractColors(data)

@app.route('/gethistori/removebg',methods=['POST'])
def getHistori_removebg():
    data = request.get_json()
    return getData.getHistori_removebg(data)

@app.route('/delhistori',methods=['POST'])
def delHistori():
    data = request.get_json()
    return getData.delHistori(data)

@app.route('/download/<file>',methods=['GET'])
def download(file):
    return  send_file('download/'+file, as_attachment=True)

@app.route('/pay/create',methods=['POST'])
def pay_create():
    data = request.get_json()
    return pay.CreatePay(data)

@app.route('/pay/check',methods=['POST'])
def pay_check():
    data = request.get_json()
    return pay.Check(data)

if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=8080)
    app.run(host='0.0.0.0', debug=True)