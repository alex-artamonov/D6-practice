from django.urls import path
from . import views
from .views import NewsList, NewsDetail, NewsF , NewsCreate, NewsDelete, NewsUpdate, upgrade_me
from .views import DefaultView, news_by_category, NewsByCategory, follow_category, NewsByAuthor, unfollow_category
 
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, 
    # позже станет ясно почему
    path('', NewsList.as_view(), name='all_news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search', NewsF.as_view(), name='search_news'),
    path('add/', NewsCreate.as_view(), name='add_news'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='edit_news'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('default/', DefaultView.as_view()),
    path('category/<int:pk>/', NewsByCategory.as_view(), name='news_by_cat'),
    path('category/<int:pk>/follow/', follow_category, name='follow_cat'),
    path('category/<int:pk>/unfollow/', unfollow_category, name='unfollow_category'),
    path('author/<int:pk>/', NewsByAuthor.as_view(), name='news_by_author'),
    ]