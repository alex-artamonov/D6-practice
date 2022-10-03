from django_filters import FilterSet
from .models import PostAuthor, Post
from django import forms
import django_filters
from django_filters.widgets import RangeWidget


class NewsFilter(FilterSet):

    # Дата_создания = django_filters.DateRangeFilter()
    created_dtm = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    
    class Meta:
        # model = PostAuthor
        model = Post
        fields = ('created_dtm', 'title', 'author_id')
        # fields = {
        #     'Дата_создания': ['gt', 'lt'],
        #     'Название_статьи': ['icontains'],
        #     'Автор': ['icontains'],
        #     # 'Имя_пользователя': ['exact'],      
        # }

        # widgets = {
            # 'Название_статьи__icontains': forms.TextInput(attrs={'class': 'form-control',}),
        #     'Автор__icontains': forms.TextInput(attrs={'class': 'form-control'}),
        #     # 'type': forms.Select(attrs={'class': 'form-control'}),
        #     # 'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        # } #
