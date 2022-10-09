from django.db.models.signals import post_save, pre_save, pre_init
from django.dispatch import receiver 
from news.models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.contrib.auth.models import Group


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
    # authors = 
    if not request.user.groups.filter(name='common').exists():
        common_group.user_set.add(user)


@receiver(post_save, sender=Post)
def notify_followers(sender, instance, created, **kwargs):
    # print('hi from notify_followers', kwargs)
    # print(f'{created =}')
    # print('hi from notify_followers', sender, instance)
    # print(f'{instance.get_absolute_url()=}')
    if created:
        link = 'http://localhost:8000' + instance.get_absolute_url()
        # print(link)
        # for cat in instance.categories.all():
            # print(get_emails_list(cat))
            # send_email(cat.name, instance.title, instance.content[:51], get_emails_list(cat), link)



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

    # print(html_content)

    msg = EmailMultiAlternatives(
        subject=f'новая статья по подписке {category_name}',
        body=content, #  это то же, что и message
        from_email='sat.arepo@yandex.ru',
        to=recipients_list,
    )
    msg.attach_alternative(html_content, "text/html") # добавляем html
    msg.send()