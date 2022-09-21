from django.urls import path
from . import views
from .views import ProductDetail, ProductsList, search
# from .views import Products
urlpatterns = [
    path('', ProductsList.as_view(),name='products'),
    path("<int:pk>", ProductDetail.as_view()),
    path('search', views.search)
]