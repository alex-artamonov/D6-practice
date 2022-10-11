# from django.utils import timezone
from django.shortcuts import redirect
import datetime
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from news.models import User, Category

DT_FORMAT = '%Y-%m-%d'
TODAY = datetime.date.today()
WEEK_AGO = TODAY + datetime.timedelta(-7)

def url_last_week(category_id):    
    # today = datetime.date.today()
    # week_ago = today + datetime.timedelta(-7)
    url_part = 'http://localhost:8000'
    url_part += redirect('search_news').url
    query_part = f'?categories={category_id}&created_dtm_min={WEEK_AGO.strftime(DT_FORMAT)}&created_dtm_max={TODAY.strftime(DT_FORMAT)}'
    # 'created_dtm_min=2022-10-03&created_dtm_max=2022-10-08'
    return url_part + query_part
    # return 'asdf'

def get_weekly_digest():
    # print(settings.TIME_ZONE)
    # week_ago = today + datetime.timedelta(days=-7)
    cats = Category.objects.filter(postcategory__isnull=False,post__created_dtm__gte=WEEK_AGO, post__created_dtm__lte=TODAY).distinct()
    cats = cats.all().values('id', 'name')
    emails = []
    for cat in cats:
        usrs = User.objects.filter(usercategory__category_id=cat['id'])
        # print(cat['name'])
        emails += [u.email for u in usrs if u.email]

    return emails

def get_emails_list(category):
    cat = category
    email_list = [user.email for user in cat.user.all()]
    return email_list


def send_email(category_name, title, content, recipients_list, link):
    html_content = render_to_string(
        'news/email_news.html',
        {'user': 'подписчик',
        'title': title,
        'category_name': category_name,
        'content': content,
        'link': link}
    )
    print('hi from send_email')

    # print(html_content)

    msg = EmailMultiAlternatives(
        subject=f'новая статья по подписке {category_name}',
        body=content, #  это то же, что и message
        from_email='sat.arepo@yandex.ru',
        to=recipients_list,
    )
    msg.attach_alternative(html_content, "text/html") # добавляем html
    msg.send()


 


    