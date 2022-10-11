from django.shortcuts import redirect
import datetime
from django.core.mail import send_mail
import my_shop.settings

import news.utils as nu
from news.models import Category, User

DT_FORMAT = '%Y-%m-%d'
TODAY = datetime.date.today()
WEEK_AGO = TODAY + datetime.timedelta(-7)


def print_hello():
    print('hi from print_hello task')
    s = 'asdf'
    print(s)
  

def print_emails():
    # my_fun.get_weekly_digest()
    # print('hi from print emails')
    s = nu.get_weekly_digest()
    # s = 'asdf'
    print(s)

def url_last_week(category_id):    
    # today = datetime.date.today()
    # week_ago = today + datetime.timedelta(-7)
    url_part = 'http://localhost:8000'
    url_part += redirect('search_news').url
    query_part = f'?categories={category_id}&created_dtm_min={WEEK_AGO.strftime(DT_FORMAT)}&created_dtm_max={TODAY.strftime(DT_FORMAT)}'
    # 'created_dtm_min=2022-10-03&created_dtm_max=2022-10-08'
    return url_part + query_part


def send_weekly_digest():
    
#     File "/usr/lib/python3.10/smtplib.py", line 908, in sendmail
#     raise SMTPDataError(code, resp)
# smtplib.SMTPDataError: (554, b'5.7.1 Message rejected under suspicion of SPAM; https://ya.cc/1IrBc #1665519620-lIqkcXR7PM-KKhqqURM')

    cats = Category.objects.filter(postcategory__isnull=False,post__created_dtm__gte=WEEK_AGO, post__created_dtm__lte=TODAY).distinct()
    cats = cats.all().values('id', 'name')
    from_email = my_shop.settings.DEFAULT_FROM_EMAIL
    emails = []
    print("кол-во категорий: ",cats.count())
    for cat in cats:
        cat_id = cat['id']
        usrs = User.objects.filter(usercategory__category_id=cat_id)
        link = url_last_week(cat_id)
        # print(cat['name'])
        emails = [u.email for u in usrs if u.email]
        # send_mail(subject=f'Еженедельная подписка по категории {cat["name"]}', 
        #     message=f'\nСсылка на новые статьи за неделю: \n{link}',
        #     from_email=from_email,
        #     recipient_list=emails,
        # )
             
        subject=f'Еженедельная подписка по категории {cat["name"]}'
        message=f'\nСсылка на новые статьи за неделю: \n{link}'
        from_email=from_email
        recipient_list=emails
        print(subject, message, from_email, recipient_list)



    
