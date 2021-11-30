from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Products
from django.contrib.auth.models import User

import json, os

JSON_PATH = 'mainapp/json'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as file:
        return json.load(file)

class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')
        Products.objects.all().delete()
        for product in products:
            category_name = product['category']
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_product = Products(**product)
            new_product.save()

        super_user = User.objects.create_superuser('django', 'djang0@mail.ru', 'geekbrains')