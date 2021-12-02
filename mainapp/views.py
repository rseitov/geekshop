from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
import os
import json
from mainapp.models import  Products, ProductCategory
from basketapp.models import Basket
# Create your views here.

module_dir = os.path.dirname(__file__,)

# links_menu = [
#         {'href': 'products_all', 'name': 'все'},
#         {'href': 'products_home', 'name': 'дом'},
#         {'href': 'products_office', 'name': 'офис'},
#         {'href': 'products_modern', 'name': 'модерн'},
#         {'href': 'products_classic', 'name': 'классика'},
#     ]

menu = [
        {'href': 'index', 'name': 'главная'},
        {'href': 'products:index', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
]

def index(request):
    context = {'title':'Магазин', 'menu':menu}
    return render(request, 'mainapp/index.html',context)

def products(request, pk=None):
    print(pk)
    title = "Продукты"
    links_menu = ProductCategory.objects.all()

    basket = []

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            products = Products.objects.all().order_by('price')
            category = {'name':'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Products.objects.filter(category__pk=pk).order_by('price')

        content = {

            "title": title,
            "links_menu":links_menu,
            "category":category,
            "products": products,
            "menu": menu,
            "basket":basket,
        }

        return render(request, "mainapp/products_list.html", content)

    same_products = Products.objects.all()[3:5]

    content = {

        "title": title,
        "links_menu": links_menu,
        "same_products": same_products,
        "menu":menu,
    }

    return render(request, 'mainapp/products.html',content)

def contact(request):
    context = {'title': 'Контакты', 'menu': menu}
    return render(request, 'mainapp/contact.html',context)

def main(request):
    title = 'главная'
    products = Products.objects.all()[:4]
    content = {'title': title, 'products': products, 'menu': menu}
    return render(request, 'mainapp/index.html', content)



