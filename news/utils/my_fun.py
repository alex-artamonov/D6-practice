from django.utils import timezone
from django.shortcuts import redirect
import datetime
from django.conf import settings

from news.models import User, UserCategory, Post, PostCategory, Category

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
    pass

def get_cats():
    # print(settings.TIME_ZONE)
    # week_ago = today + datetime.timedelta(days=-7)
    cats = Category.objects.filter(postcategory__isnull=False,post__created_dtm__gte=WEEK_AGO, post__created_dtm__lte=TODAY).distinct()
    cats = cats.all().values('id', 'name')
    for cat in cats:
        usrs = User.objects.filter(usercategory__category_id=cat['id'])
        print(cat['name'])
        print([u.email for u in usrs if u.email])


 


    