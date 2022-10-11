from django.db.models.signals import post_save
from django.dispatch import receiver 
from news.models import Post
from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.contrib.auth.models import Group

import news.utils as nu


# @receiver(pre_init, sender=Post)
# def cancel_init(sender, **kwargs):
#     print('hi cancel_init', kwargs)
#     return redirect('/')


# @receiver(pre_save, sender=Post)
# def cancel_save(sender, **kwargs):
#     print('hi from cancel_save', kwargs)
    
    # raise Exception('OMG')


@receiver(user_signed_up)
def send_welcome(request, user, **kwargs):
    # print('hi from user_signed_up', user, user.email, kwargs)
    send_mail(
        message=f'Уважаемый {user.username}, добро пожаловать на наш сайт.',
        subject='registration at example.com',
        from_email='sat.arepo@yandex.ru',
        recipient_list=[user.email]
    )
    common_group = Group.objects.get(name='common')
   
    if not request.user.groups.filter(name='common').exists():
        common_group.user_set.add(user)


@receiver(post_save, sender=Post)
def notify_followers(sender, instance, created, **kwargs):
    # if not created:
        # print('hi from notify_followers', kwargs)
        # print(f'{created =}')
        # print('hi from notify_followers', sender, instance)
        # print(f'{instance.get_absolute_url()=}')
    if created:
        link = 'http://localhost:8000' + instance.get_absolute_url()
        # print('hi from created:', link)
        for cat in instance.categories.all():
            # print(nu.get_emails_list(cat))
            nu.send_email(cat.name, instance.title, instance.content[:51], 
            nu.get_emails_list(cat), link)



