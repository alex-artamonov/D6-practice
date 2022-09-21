from django_filters import FilterSet
from .models import PostAuthor

class NewsFilter(FilterSet):
    
    class Meta:
        model = PostAuthor
        # fields = ('created_dtm', 'title', 'author_id.)
        fields = {
            'Дата_создания': ['gt', 'lt'],
            'Название_статьи': ['icontains'],
            'Автор': ['icontains'],
            'Имя_пользователя': ['exact']
        }
