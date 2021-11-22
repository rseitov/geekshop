from django.shortcuts import render
from django.templatetags.static import static
import os
import json

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
        {'href': 'products', 'name': 'продукты'},
        {'href': 'contact', 'name': 'контакты'},
]

def index(request):
    context = {'title':'Магазин', 'menu':menu}
    return render(request, 'mainapp/index.html',context)

def products(request):
    file_path = os.path.join(module_dir,'fixtures/products.json')
    products = json.load(open(file_path, encoding='utf-8'))

    # products = [
    #
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.', 'img': static('img/product-1.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-2.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-3.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-4.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-21.jpg')},
    #     {'name': 'Стул повышенного качества', 'text':'Не оторваться.','img': static('img/product-11.jpg')},
    # ]

    content = {
            'title': 'Продукты',
            'links_menu': links_menu,
            'products':products,
            'menu':menu,
        }



    return render(request, 'mainapp/products.html',content)

def contact(request):
    context = {'title': 'Контакты', 'menu': menu}
    return render(request, 'mainapp/contact.html',context)

