from django.urls import path
from . import views
from .views import NewsList, NewsDetail, NewsF , NewsCreate, NewsDelete, NewsUpdate
 
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, 
    # позже станет ясно почему
    path('', NewsList.as_view(), name='all_news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search', NewsF.as_view(), name='search_news'),
    path('add/', NewsCreate.as_view(), name='add_news'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='edit_news'),
    ]