from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authnapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Products, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from authnapp.forms import ShopUserRegisterForm, ShopUserEditForm
from adminapp.forms import ShopUserAdminForm, ProductEditForm, ProductCategoryEditForm
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
# Create your views here.

# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователей'
#
#     user_list = ShopUser.objects.all().order_by('-is_active','-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': user_list
#     }
#
#     return render(request, 'adminapp/users.html', content)

class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователь/создание'

    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title':title, 'update_form': user_form }

    return render(request, 'adminapp/user_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == "POST":
        edit_form = ShopUserAdminForm(request.POST, request.FILES, instance=edit_user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminForm(instance=edit_user)

    content = {
        'title':title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователей/удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title':title,
        'user_to_delete': user
    }

    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {

        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)

@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    pass

@user_passes_test(lambda u: u.is_superuser)
def category_update(request):
    pass

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request):
    pass

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)

    products_list = Products.objects.filter(category__pk = pk).order_by('name')

    content = {

        'title': title,
        'category': category,
        'objects' : products_list
    }

    return render(request, 'adminapp/products.html', content)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = "__all__"

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категорий/редактирование'

        return context

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(DetailView):
    model = Products
    template_name = 'adminapp/product_read.html'



@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукты/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args = [pk]))
    else:
        product_form = ProductEditForm( initial = {'category': category})

    content = {
        'title': title,
        'update_form': product_form,
        'category': category
    }

    return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукты/подробнее'
    product = get_object_or_404(Products, pk=pk)
    content = {'title': title, 'object': product}

    return render(request, 'adminapp/product_read.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукты/редактирование'

    edit_product = get_object_or_404(Products, pk=pk)

    if request.method == "POST":
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category
    }

    return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Products, pk=pk)

    if request.method == "POST":
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products',  args=[product.category.pk]))

    content = {'title': title, 'product_to_delete': product }

    return render(request, 'adminapp/product_delete.html', content)