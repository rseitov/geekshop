from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
import os
import json
from mainapp.models import  Products, ProductCategory
# Create your views here.

module_dir = os.path.dirname(__file__,)

links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

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
    # file_path = os.path.join(module_dir,'fixtures/products.json')
    # products = json.load(open(file_path, encoding='utf-8'))

    # products = [
    #    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-3.jpg')},

    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.', 'img': static('img/product-1.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-2.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-4.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-21.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-11.jpg')},
    # ]
    product = Products.objects.all()[:4]
    content = {
            'title': 'Продукт',
            'links_menu': links_menu,
            'products':product,
            'menu':menu,
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



