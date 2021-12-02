from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from basketapp.models import  Basket
from mainapp.models import Products
# Create your views here.


def basket(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)

def basket_add(request, pk):
    product = get_object_or_404(Products, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def basket_remove(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)