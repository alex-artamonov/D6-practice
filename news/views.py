# from operator import methodcaller
from django.http import HttpResponse
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
from django.utils import timezone
import datetime


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
        # print(Category.objects.exclude(pk__in=list(current_user.category_set.values_list(flat=True))))
        context['user_has_no_categories'] = Category.objects.exclude(pk__in=list(current_user.category_set.values_list(flat=True)))
        # context['current_category'] = self.request.GET.get['ca']
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
        # print(self.request.GET)
        qs = super().get_queryset(**kwargs)
        return qs.filter(categories=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
    #     news = Post.objects.filter(categories=self.kwargs.get('pk'))
    #     self.queryset = news

        context = super().get_context_data(**kwargs)
        context['current_category'] = Category.objects.get(pk=self.kwargs.get('pk'))
        
    #     context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
    #     context['categories'] = Category.objects.all() 
    #     context['news_count'] = news.count
    #     context['authors'] = Author.objects.all()
        return context


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

 


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'news/news_create.html'
    form_class = NewsForm
    permission_required = ('news.add_post', )

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        context['categories'] = Category.objects.annotate(cnt=Count('post'))
        context['news_count'] = Post.objects.all().count
        # context['authors'] = Group.objects.get(name='authors')
        context['authors'] = Author.objects.annotate(cnt=Count('post'))
        current_user = User.objects.get(pk=self.request.user.id)

        return context

    def form_valid(self, form):
        today = timezone.now()
        author = Author.objects.get(user__id=self.request.user.id)
        too_many_posts = author.post_set.filter(
            created_dtm__range=(today - datetime.timedelta(days=3), today)
            ).count() > 2 # по условию должно быть не более 3 - видимо на том этапе БД не получила запись
        
        if too_many_posts:
            # return redirect('/')
            return HttpResponse("too many posts today")
        else:            
            # print(author)
            form.instance.author = author
            return super().form_valid(form)




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
    template_name = 'news/news_filter.html'
    context_object_name = 'news'
    



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
    # authors = 
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user).save()
        # print(user)
    return redirect('/')


def follow_category(request, pk):
    # for it in request:
    user = request.user
    category = Category.objects.get(id=pk)
    user.category_set.add(category)
    return redirect(category)
        

def unfollow_category(request, pk):
    # for it in request:
    user = request.user
    category = Category.objects.get(id=pk)
    user.category_set.remove(category)
    return redirect('/')       

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

def generate_query_last_week(category_id):
    DT_FORMAT = '%Y-%m-%d'
    today = datetime.date.today()
    week_ago = today + datetime.timedelta(-7)
    url_part = 'http://localhost:8000'
    url_part += redirect('search_news').url
    query_part = f'?categories={category_id}&created_dtm_min={week_ago.strftime(DT_FORMAT)}&created_dtm_max={today.strftime(DT_FORMAT)}'
    # 'created_dtm_min=2022-10-03&created_dtm_max=2022-10-08'
    return url_part + query_part
    # return 'asdf'
