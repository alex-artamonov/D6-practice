from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# from django.core import Paginator
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.

# class Products(View):
#     def get(self, request):
#         products = Product.objects.order_by('-price')
#         p = paginator(products, 1)
#         products = p.get_page(request.GET('page', 1))
#         data = {
#             'products': products
#         }
#         return render(request, 'products.html', data)

class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


def search(request):
    return HttpResponse("This is supposed to be the search page")