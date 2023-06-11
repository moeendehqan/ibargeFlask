import pymongo
import pandas as pd
client = pymongo.MongoClient()
db = client['barge2']



#db['randomText'].delete_many({'type':'wrd'})
lis = ['فراموش','سلام','خودرو','ماه','عسل','عصا','کمد','کشو','آب','کاسه','عکس','برگ','برگه','تلفن','عینک','صندلی','خویشتن','کوه','دشت','دریا','صدا','هوا','اجتناب','رایانه','کار',
       'شب','روز','سپیده','اعدام','نهال','درخت','گیاه','موزه','خیابان','استخر','کافه','پارک','روستا','شهر','کلان','فرودگاه','نان','لوبیا','عدس','نخود','حنبش','جاذبه','گرانش','سیاه',
       'سفید','سیاه','زرد','سبز','آبی','قرمز','قهوه ای','قهوه','موز','گوجه','صابون','شامپو','شیره','تریاک','گل','گلدون','گلاب','گلایول','گوجه','سیب','توت','شبنشین','پاتوق','پنکه','کولر',
       'خبر','خانم','آقا','آفتاب','سرامیک','سوت','سرداب','کشور','قاره','قرن','تاریخ','جغرافی','دنیا','جهان','کیهان','کانون','مرکز','سازمان','صاحب','حیوان','مرغ','مدرن','شراب','شهید',
       'شجاعت','ترس','خشم','خجالت','خدا','پیامبر','کتاب','دفتر','مداد','خودکار','خرید','فروش','بازار','معامله','عضو','کیف','لباس','لایحه','چراغ','تیر','اسلحه','سنگین','سبک','رود','راننده'
       ,'گوش','حلق','بینی','چشم','لبخند','فرش','موکت','تابلو','پل','پارچه','نخ','سیگار','فندک','پاکت','مغازه','گوسفند','مورچه','سگ','فیل','فسیل','قورباغه','قدرت','سرعت','دقت','قانون',
       'حکیم','کلاس','سال','سحر','لوله','لبنیات','لیسانس','لکه','ننگ','نامحرم','منسجم','قالی','خاک','خون','نمک','نمره','یاداشت','سماور','واسطه','بیان','کمال','جنسیت','سیاست','قطار',
       'اجتماع','مدنی','قضایی','پلیس','پیوند','رئیس','نبوغ','نادم','مبحوس','زندان','سماق','چای','رفیق','دوست','محبت','شعار','شمایل','غم','شاد','خفا','خفته','خیار','چهارپا','فصل','هفته'
       ,'سکه','اسکناس','برات','چاقو','قاشق','صوت','سرهنگ','ارتش','زرهی','هنگ','کلانتر','تانک','دزد','کلید','کافر','روحانی','شماره','کاهگل','کافور','کاستن','کاشتن','کیفر','مهم','مبهم',
       'مسکو','مالیات','مانده','ماست','ضمیر','ضمانت','ضامن','صادر','صفا','ثبات','قفل','قند','فرفره','فاسد','عمر','عامر','عمه','عهد','عصر','هنر','همایش','هستی','هند','خاور','خجالت',
       'حبس','حس','جمال','جهاد','جلاد','چشمه','چاشت','شیر','شاه','شیفته','شاهد','سیر','ساحر','سر','ساده','سیل','سیمان','باد','بیل','باور','باشگاه','بحران','لازم','اوند','اروند','تیشه',
       'تئاتر','نغمه','نسیم','نهاد','منزل','مشکوک','معصوم','کادر','کفش','کود','گهواره','گور','طلاق','طلاب','زرد','زیاد','زود','زاویه','روشد','ریش','رانش','دعا','دوا','دور','دود','دادستان'
       ,'وافر','وضعیت','واعظ','طیور','حاتم','وحشی','حافظ','مجنون','شیرین','تلخ','ترش','شور','گز','کیک','هوش','ذکاوت','حیا','شیشه','چوب','آهن','فولاد','مس','گرم','یخ','سرد','شیوا','گونه'
       ,'بوسه']

df = pd.DataFrame(columns=['text'],data=lis)
df['id'] = df.index+250
df['len'] = [len(x) for x in df['text']]
df['type'] = 'wrd'
db['randomText'].insert_many(df.to_dict('records'))
print(df)