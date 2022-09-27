from django.db import models as m
from django.contrib.auth.models import User
from django.db.models import Sum



# Create your models here.

class Author(m.Model):
    user = m.OneToOneField(User, on_delete=m.CASCADE)
    rating = m.SmallIntegerField(default=0)

    def update_rating(self):
        post_rating_sum = self.post_set.all().aggregate(post_rating=Sum('rating'))
        comment_rating_sum = self.user.comment_set.all().aggregate(comment_rating=Sum('rating'))
        self.rating = post_rating_sum.get('post_rating') * 3 + comment_rating_sum.get('comment_rating')
        self.save()

    def __str__(self) -> str:
        return f"{self.user.last_name} {self.user.first_name}"

    
class Category(m.Model):
    name = m.CharField(max_length=30, unique=True)
    user = m.ManyToManyField(User, through='UserCategory')

    def __str__(self) -> str:
        return self.name

class UserCategory(m.Model):
    category = m.ForeignKey(Category, on_delete=m.CASCADE)
    user = m.ForeignKey(User, on_delete=m.CASCADE)

class Post(m.Model):
    NEWS = 'NWS'
    ARTICLE = 'ACL'
    TYPES = [
        (NEWS, 'новость'),
        (ARTICLE, 'статья')
    ]
    author = m.ForeignKey(Author, on_delete=m.CASCADE)
    type = m.CharField(max_length=3, choices=TYPES)
    created_dtm = m.DateTimeField(auto_now_add=True)
    title = m.CharField(max_length=255)
    content = m.TextField()
    categories = m.ManyToManyField(Category, through='PostCategory')
    rating = m.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.title=}, {self.type=}"

    def preview(self):
        return self.content[:124] + '...'

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def get_absolute_url(self): # добавим абсолютный путь, 
        #чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}' 

class PostCategory(m.Model):
    post = m.ForeignKey(Post, on_delete=m.CASCADE)
    category = m.ForeignKey(Category, on_delete=m.CASCADE)



class Comment(m.Model):
    post = m.ForeignKey(Post, on_delete=m.CASCADE)
    user = m.ForeignKey(User, on_delete=m.CASCADE)
    text = m.TextField()
    created_dtm = m.DateTimeField(auto_now_add=True)
    rating = m.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def __str__(self):
        return f"by {self.user.username} at {self.created_dtm.strftime('%Y-%m-%d %H:%M:%S')}"


class PostAuthor(m.Model):
    id = m.BigIntegerField(primary_key=True)
    Название_статьи = m.CharField(max_length=255)
    Дата_создания = m.DateTimeField(auto_now_add=False)
    Имя_пользователя = m.CharField(max_length=50)
    Автор = m.CharField(max_length=40)
    content = m.TextField()

    def save(self, *args, **kwargs):
        raise NotSupportedError('This model is tied to a view, it cannot be saved.')

    class Meta:
        managed = False
        db_table = 'vw_news_filter'
        # verbose_name = 'Example'
        # verbose_name_plural = 'Examples'
        # ordering = ['name']