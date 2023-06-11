
from Login import getUserByPUA
import cv2
import numpy as np
from persiantools.jdatetime import JalaliDate
import datetime
import random
import pytesseract
import pymongo
from pdf2docx import Converter
from PyPDF2 import PdfReader, PdfWriter
import arabic_reshaper
from bidi.algorithm import get_display
from docx import Document
from hijri_converter import Hijri, Gregorian
import function
from PIL import Image
import os
from pypdf import PdfMerger
from Pylette import extract_colors


client = pymongo.MongoClient()
db = client['barge2']
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
folderDownload = 'download/'

def CheckUserForApi(pua,vip=False):
    user = getUserByPUA(pua)
    if user['replay'] == False:
        return {'replay':False,'msg':'مشکل در اطلاعات کاربری لطفا مجدد وارد شوید'}

    if vip and user['user']['creditDay']==0:
            return {'replay':False,'msg':'برای استفاده از این سرویس اعتبار کافی نمیباشد'}
    return {'replay':True,'user':user}

def getHistoriByPhone(phone,section,limit):
     return [x for x in db['histori'].find({'phone':phone,'section':section},{'_id':0,'result':1,'filesName':1,'JalaliDate':1}).sort('datatime',-1).limit(limit)]


def imageToText(file,pua,option):
    if file.filename.split('.')[-1] not in ['jpg','png','jpeg']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    img = file.read()
    dic = {'phone':check['user']['user']['phone'],'section':'imagetotext','filesName':file.filename,
           'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
           'size':int(len(img)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'text'}
    img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
    text = pytesseract.image_to_string(img,lang=option)
    dic['result'] = text
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'imagetotext',5)
    return {'replay':True,'result':text,'histori':histori}

def pdfToWord(file,pua,option):
    if file.filename.split('.')[-1] not in ['pdf']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    pdf = file.read()
    dic = {'phone':check['user']['user']['phone'],'section':'pdftoword','filesName':file.filename,
        'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
        'size':int(len(pdf)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'link'}
    fileDir ='fileStorege/'+dic['filesName']+'-'+str(dic['id'])+'.pdf'
    open(fileDir, 'wb').write(pdf)
    outpath = folderDownload+str(dic['id'])+'.docx'
    if option=='eng':
        cv = Converter(fileDir)
        cv.convert(outpath, start=0, end=None)
    else:
        pdf = PdfReader(fileDir)
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            page_text = arabic_reshaper.reshape(page_text)
            text += get_display(page_text)
        doc = Document()
        doc.add_paragraph(text)
        doc.save(outpath)
    dic['result'] = str(dic['id'])+'.docx'
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'pdftoword',5)
    return {'replay':True,'result':dic['result'],'histori':histori}


def convertDate(data):
    check = CheckUserForApi(data['pua'])
    if check['replay'] == False: return check
    dic = {'phone':check['user']['user']['phone'],'section':'convertdate','filesName':data['date'],
        'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
        'size':0,'id':random.randint(1000000000, 9999999999),'result':'','resultType':'data'}
    now = datetime.datetime.fromtimestamp(int(data['date'])/1000)

    miladi = str(now).split(' ')[0]
    miladiStrMonth = str(now.month).replace('1','January').replace('2','February').replace('3','March').replace('4','April').replace('5','May').replace('6','June').replace('7','July').replace('8','August').replace('9','September').replace('10','October').replace('11','November').replace('12','December')
    miladiStrWeek = str(now.weekday()).replace('0','Monday').replace('1','Tuesday').replace('2','Wednesday').replace('3','Thursday').replace('4','Friday').replace('5','Saturday').replace('6','Sunday')
    miladiStr = str(now.year) + ' '+ miladiStrMonth + ' '+ str(now.day) + ' '+'،' + miladiStrWeek
    miladi = {'int':miladi,'str':miladiStr}

    jalali = JalaliDate.to_jalali(now.year,now.month,now.day)
    jalaliStrMonth = str(jalali.month).replace('1','فروردین').replace('2','اردیبهشت').replace('3','خرداد').replace('4','تیر').replace('5','مرداد').replace('6','شهریور').replace('7','مهر').replace('8','آبان').replace('9','آذر').replace('10','دی').replace('11','بهمن').replace('12','اسفند')
    jalaliStrWeek = str(jalali.weekday()).replace('0','شنبه').replace('1','یکشنبه').replace('2','دوشنبه').replace('3','سه شنبه').replace('4','چهارشنبه').replace('5','پنجشنبه').replace('6','جمعه')
    jalaliStr = str(jalali.year) + ' '+ jalaliStrMonth + ' '+ str(jalali.day) + ' '+'،' + jalaliStrWeek
    jalali = {'int':str(jalali),'str':jalaliStr}

    borjname = str(JalaliDate.to_jalali(now.year,now.month,now.day).month)
    if len(borjname) == 1: borjname = '0'+borjname
    borjFilename = (str(JalaliDate.to_jalali(now.year,now.month,now.day).month))
    if len(borjFilename) == 1: borjFilename = '0'+borjFilename

    borjname = borjname.replace('01','حَمَل').replace('02','ثَور').replace('03','جوزا').replace('04','سرطان').replace('05','اسد').replace('06','سنبله').replace('07','میزان').replace('08','عقرب').replace('09','قوس ').replace('10','جدی').replace('11','دلو').replace('12','حوت')
    borjFilename = borjFilename.replace('01','hamal.svg').replace('02','sor.svg').replace('03','joza.svg').replace('04','saratan.svg').replace('05','asad.svg').replace('06','sonbole.svg').replace('07','mizan.svg').replace('08','aghrab.svg').replace('09','ghos.svg').replace('10','jedi.svg').replace('11','delo.svg').replace('12','hot.svg')
    borj = {'borjname':borjname,'borjFilename':borjFilename}

    hijri = Gregorian(now.year,now.month,now.day).to_hijri()
    hijriStrMonth = str(hijri.month).replace('01','محرّم').replace('02','صفر').replace('03','ربیع الاول').replace('04','ربیع الثانی').replace('05','جمادی الاولی').replace('06','جمادی الثانی').replace('07','رجب').replace('08','شعبان').replace('09','رمضان').replace('10','شوال').replace('11','ذی القعده').replace('12','ذی الحجه')
    hijriStrWeek = str(now.weekday()).replace('0','الأثنين').replace('1','الثلاثاء').replace('2','الأربعاء').replace('3','الخميس').replace('4','الجمعه').replace('5','السبت').replace('6','الأحد')
    jalaliStr = str(hijri.year) + ' '+ hijriStrMonth + ' '+ str(hijri.day) + ' '+'،' + hijriStrWeek
    hijri = {'int':str(hijri),'str':jalaliStr}

    result = {'jalali':jalali,'miladi':miladi,'hijri':hijri,'borj':borj}
    dic['result'] = result
    db['histori'].insert_one(dic)

    return {'replay':True,'result':result}


def loremIpsum(data):
    check = CheckUserForApi(data['pua'])
    if check['replay'] == False: return check
    dic = {'phone':check['user']['user']['phone'],'section':'loremipsum','filesName':data['option'],
        'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
        'size':0,'id':random.randint(1000000000, 9999999999),'result':'','resultType':'text'}
    textDb = [x['text'] for x in db['randomText'].find({'type':data['option']},{'_id':0,'text':1})]
    text = ''
    for i in range(0,int(data['amount'])):
        text = text + textDb[random.randint(0, len(textDb))] + '\n'
    dic['result'] = text
    db['histori'].insert_one(dic)
    return {'replay':True,'result':text}


def pdfToText(file,pua,option):
    if file.filename.split('.')[-1] not in ['pdf']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    pdf = file.read()
    dic = {'phone':check['user']['user']['phone'],'section':'pdftotext','filesName':file.filename,
        'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
        'size':int(len(pdf)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'text'}
    fileDir ='fileStorege/'+str(dic['id'])+'.pdf'
    open(fileDir, 'wb').write(pdf)

    reader = PdfReader(fileDir)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    dic['result'] = text
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'pdftotext',5)
    return {'replay':True,'result':dic['result'],'histori':histori}



def compressimage(file,pua,option):
    if file.filename.split('.')[-1] not in ['jpg','png','jpeg']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    img = file.read()
    dic = {'phone':check['user']['user']['phone'],'section':'compressimage','filesName':file.filename,
           'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
           'size':int(len(img)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'link'}
    fileDir ='fileStorege/'+str(dic['id'])+file.filename
    img = cv2.imdecode(np.frombuffer(img, np.uint8), -1)
    cv2.imwrite(fileDir,img)
    image = Image.open(fileDir)
    outpath = 'download/'+str(dic['id'])+(file.filename.split('.')[0])+'.jpg'
    image.save(outpath, optimize=True, quality=int(int(option)/2))
    image = Image.open('download/'+str(dic['id'])+(file.filename.split('.')[0])+'.jpg')
    befor_volume = dic['size']
    after_volume = int(os.stat(outpath).st_size/1.024)
    compress = int((1-(after_volume / befor_volume))*100)
    if compress<0:
        compress = abs(compress)
        msg = f'حجم تصویر {compress} درصد افزایش و بهینه تر شد'
    else:msg = f'حجم تصویر {compress} درصد کاهش یافت'
    dic['result'] = str(dic['id'])+(file.filename.split('.')[0])+'.jpg'
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'compressimage',5)
    return {'replay':True,'result':dic['result'],'histori':histori,'msg':msg}

def imagefrompdf(file,pua):
    if file.filename.split('.')[-1] not in ['pdf']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    pdf = file.read()
    dic = {'phone':check['user']['user']['phone'],'section':'imagefrompdf','filesName':file.filename,
           'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
           'size':int(len(pdf)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'link'}
    fileDir ='fileStorege/'+str(dic['id'])+file.filename
    open(fileDir, 'wb').write(pdf)
    outpath = 'download/'+str(dic['id'])+(file.filename.split('.')[0])+'.zip'
    try:image_counter = function.extract_images_from_pdf(fileDir,outpath)
    except:image_counter = 0
    if image_counter == 0:
        print(image_counter)
        return {'replay':False,'msg':'تصویری در فایل پی دی اف یافت نشد'}
    dic['result'] = str(dic['id'])+(file.filename.split('.')[0])+'.zip'
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'imagefrompdf',5)
    msg = f'تعداد {image_counter} تصویر استخراج شد'
    return {'replay':True,'result':dic['result'],'histori':histori, 'msg':msg}


def compresspdf(file,pua):
    if file.filename.split('.')[-1] not in ['pdf']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    pdf = file.read()
    dic = {'phone':check['user']['user']['phone'],'section':'compresspdf','filesName':file.filename,
           'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
           'size':int(len(pdf)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'link'}
    fileDir ='fileStorege/'+str(dic['id'])+file.filename
    open(fileDir, 'wb').write(pdf)
    outpath = 'download/'+str(dic['id'])+'.pdf'
    reader = PdfReader(fileDir)
    writer = PdfWriter()
    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)
    with open(outpath, "wb") as f:
        writer.write(f)
    dic['result'] = str(dic['id'])+'.pdf'
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'compresspdf',5)
    return {'replay':True,'result':dic['result'],'histori':histori}



def mergepdf(file1,file2,pua):
    if file1.filename.split('.')[-1] not in ['pdf']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    if file2.filename.split('.')[-1] not in ['pdf']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    pdf1 = file1.read()
    pdf2 = file2.read()
    dic = {'phone':check['user']['user']['phone'],'section':'mergepdf','filesName':file1.filename,
           'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
           'size':int(len(pdf1)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'link'}
    fileDir1 ='fileStorege/'+str(dic['id'])+file1.filename
    fileDir2 ='fileStorege/'+str(dic['id'])+file1.filename
    open(fileDir1, 'wb').write(pdf1)
    open(fileDir2, 'wb').write(pdf2)
    merger = PdfMerger()
    merger.append(fileDir1)
    merger.append(fileDir2)
    outpath = 'download/'+str(dic['id'])+'.pdf'
    merger.write(outpath)
    merger.close()
    dic['result'] = str(dic['id'])+'.pdf'
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'mergepdf',5)
    return {'replay':True,'result':dic['result'],'histori':histori}

def extractColors(file,option,pua):
    if file.filename.split('.')[-1] not in ['jpg','png','jpeg']:return {'replay':False,'msg':'فرمت فایل مجاز نیست'}
    check = CheckUserForApi(pua)
    if check['replay'] == False: return check
    img = file.read()

    dic = {'phone':check['user']['user']['phone'],'section':'extractcolors','filesName':file.filename,
           'JalaliDate':JalaliDate.today().isoformat(),'datatime':datetime.datetime.now().ctime(),
           'size':int(len(img)/1.024),'id':random.randint(1000000000, 9999999999),'result':'','resultType':'data'}
    fileDir ='fileStorege/'+str(dic['id'])+file.filename
    open(fileDir, 'wb').write(img)
    pallet = extract_colors(fileDir, palette_size=int(option), resize=True, mode='MC', sort_mode='luminance')
    result = []
    for i in pallet:
        result.append(i.rgb)
    dic['result'] = result
    print(result)
    db['histori'].insert_one(dic)
    histori = getHistoriByPhone(check['user']['user']['phone'],'extractcolors',5)
    return {'replay':True,'result':result,'histori':histori}