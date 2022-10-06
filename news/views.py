# from operator import methodcaller
# from django.http import HttpResponse
#from re import I
import re
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *
from .filters import NewsFilter
from .forms import NewsForm

# Create your views here.

class CustomContextMixin():
    def get_context_data(self, **kwargs):
        news = Post.objects.filter(categories=self.kwargs.get('pk'))
        # user_category = UserCategory.objects.filter()
        # news = Post.objects.all()
        # self.queryset = news

        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        # context['categories'] = Category.objects.all()
        context['categories'] = Category.objects.annotate(cnt=Count('post')) #.filter(cnt__gt=0)
        context['news_count'] = news.count
        context['authors'] = Author.objects.annotate(cnt=Count('post'))
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        authors_list = [a.user.last_name + ', ' + a.user.first_name for a in Author.objects.all()]
        context['authors_list'] = authors_list
        current_user = User.objects.get(pk=self.request.user.id)
        context['cats_by_user'] = current_user.category_set.all()
        return context

def news_by_category(request, cat_id):
    news = Post.objects.filter(categories=cat_id)
    cats = Category.objects.all()
    context = {
        'news': news,
        'categories': cats,
    }
    return render(request, 'news/news.html', context)


class NewsByCategory(LoginRequiredMixin, CustomContextMixin, ListView):
    # queryset = Post.objects.all()
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(categories=self.kwargs.get('pk'))

    # def get_context_data(self, **kwargs):
    #     news = Post.objects.filter(categories=self.kwargs.get('pk'))
    #     self.queryset = news

    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
    #     context['categories'] = Category.objects.all() 
    #     context['news_count'] = news.count
    #     context['authors'] = Author.objects.all()
    #     return context


class NewsByAuthor(LoginRequiredMixin, CustomContextMixin, ListView):
    # queryset = Post.objects.all()
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(author_id=self.kwargs.get('pk'))



class NewsList(LoginRequiredMixin, CustomContextMixin, ListView):
    # model = Post
    queryset = Post.objects.order_by('-created_dtm')
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_count'] = Post.objects.all().count
        return context


    def post(self, request, *args, **kwargs):
        # print(self.request['name'])
        return super().get(request, *args, **kwargs)


class NewsDetail(LoginRequiredMixin, CustomContextMixin, DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'

    # def get_context_data(self, **kwargs):        
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
    #     context['categories'] = Category.objects.all()
    #     context['news_count'] = Post.objects.all().count
    #     context['authors'] = Author.objects.all()
    #     return context


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, CustomContextMixin, UpdateView):
    template_name = 'news/news_create.html'
    form_class = NewsForm
    permission_required = ('news.change_post', )
    queryset = Post.objects.order_by('-created_dtm')
 
    # метод get_object мы используем вместо queryset, 
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # def get_context_data(self, **kwargs):        
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
    #     context['categories'] = Category.objects.all()
    #     context['news_count'] = Post.objects.all().count
    #     context['authors'] = Author.objects.all()
    #     return context


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/news_create.html'
    form_class = NewsForm
    permission_required = ('news.add_post', )

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        context['categories'] = Category.objects.all()
        context['news_count'] = Post.objects.all().count
        # context['authors'] = Group.objects.get(name='authors')
        context['authors'] = Author.objects.all()
        return context

    # def get(self, request, *args, **kwargs):
    #     file_to_render = 'news/email_news.html'
    #     return render(request, file_to_render, {})

    def post(self, request, *args, **kwargs):
        user = self.request.user.username
        title = self.request.POST['title']
        content = self.request.POST['content']
        # print(self.request.POST)
        recipients_list = []
        categories = self.request.POST.getlist('categories')
        for cat in categories:            
            category = Category.objects.get(pk=cat)
            # print(f'{category.name = }')
            recipients_list = get_emails_list(category)
            send_email(user, category.name, title, content, recipients_list)
         

        # получем наш html
        # html_content = render_to_string(
        #     'news/email_news.html',
        #     {'user': user,
        #     'title': title,
        #     'content': content,}
        # )

        # # send_mail( 
        # #     subject=f'{request.POST["title"]}',  
        # #     message=request.POST["content"], 
        # #     from_email='sat.arepo@yandex.ru',
        # #     recipient_list=[request.user.email]
        # # )

        # msg = EmailMultiAlternatives(
        #     subject=f'новая статья по подписке',
        #     body=content, #  это то же, что и message
        #     from_email='sat.arepo@yandex.ru',
        #     to=[request.user.email],
        # )
        # msg.attach_alternative(html_content, "text/html") # добавляем html
        # msg.send()

        return super().post(request, *args, **kwargs)
        # pass


    # def post(self, request, *args, **kwargs):
    #     add_notice = ''

class CategorySubscribe():
    pass

class NewsDelete(LoginRequiredMixin, DeleteView):
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class ProductDeleteView(DeleteView):
    template_name = 'news/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class NewsF(LoginRequiredMixin, CustomContextMixin, ListView):
    # queryset = PostAuthor.objects.order_by('-Дата_создания')
    queryset = Post.objects.order_by('-created_dtm')
    # queryset = Post.objects.all()
    # model = Post
    # ordering = ['created_dtm']
    template_name = 'news/news_filter.html'
    context_object_name = 'news'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
    #     authors_list = [a.user.last_name + ', ' + a.user.first_name for a in Author.objects.all()]
    #     context['authors_list'] = authors_list
    #     authors = Author.objects.all()
    #     context['authors'] = authors
    #     categories = Category.objects.all()
    #     context['categories'] = categories
    #     return context


class DefaultView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/default.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        context['one'] = 'first'
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author(user=user).save()
        # print(user)
    return redirect('/')


def follow_category(request, pk):
    # for it in request:
    user = request.user
    category = Category.objects.get(id=pk)
    user.category_set.add(category)
    return redirect(category)
        

    # def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя 
    #     # метод get_context_data у наследуемого класса
    #     context = super().get_context_data(**kwargs)
    #      # вписываем наш фильтр в контекст
    #     context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
    #     return context


def search(request):
    news_list = Post.objects.order_by('-created_dtm')
    output = '===='.join([str(p) for p in news_list])
    return HttpResponse(output)



def get_emails_list(category):
    cat = category
    email_list = [user.email for user in cat.user.all()]
    return email_list


def send_email(user, category_name, title, content, recipients_list):
    html_content = render_to_string(
        'news/email_news.html',
        {'user': user,
        'title': title,
        'catogory_name': category_name,
        'content': content,}
    )
    msg = EmailMultiAlternatives(
        subject=f'новая статья по подписке {category_name}',
        body=content, #  это то же, что и message
        from_email='sat.arepo@yandex.ru',
        to=recipients_list,
    )
    msg.attach_alternative(html_content, "text/html") # добавляем html
    msg.send()