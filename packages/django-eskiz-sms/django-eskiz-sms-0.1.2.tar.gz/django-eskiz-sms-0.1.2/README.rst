Djangodan EskizUz yordamida SMS yuborish uchun eng mukammal paket

Paketni pip install django-eskiz-sms deb o'rnatib,
asosiy appni settings.py ida INSTALLED_APPS ga eskiz_sms deb qo'shing.

Makemigration va migratedan keyin django adminga o'ting.
Makemigrationda xato bersa requests paketini ham pip install requests qilib o'rnatib oling!
U yerda EskizSMS degan modelga EskizUZ emailingiz va kabinetdan olgan parolingizni kiriting.

So'ngra asosiy urls.py ga eskiz_sms.urls ni include qiling, bu sms browserda forma orqali sms
yuborib sinab ko'rish uchun. Xavfsizlik yuzasidan keyin uni uzib qo'ying.

Odatiy ishlatish uchun istalgan joyda from eskiz_sms.views import send_sms yoki boshqa
yo'l bilan send_sms() degan metodni chaqirib ishlating. Qolgan ishlarni o'zi bajaradi.
Shuningdek admin panelda SMSLog orqali jo'natilgan SMSlar statistikasini ko'rib tursangiz bo'ladi.

Ishlatish uchun batafsil qo'llanma: https://docs.tijorat.org/django-eskiz-sms