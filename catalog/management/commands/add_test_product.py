import os
import json
from django.core.management.base import BaseCommand
from catalog.models import Products, Category

class Command(BaseCommand):
    help = 'Add test products in database'

    def handle(self, *args, **kwargs):
        #Предварительная чистка продуктов(или Category)
        Products.objects.all().delete()


        #ПОЛУЧЕНИЕ НУЖНОЙ КАТЕГОРИИ
        category, _ = Category.objects.get_or_create(name='Бытовая техника')

        products = [
            {"name": "Tefal FV1R10F1", "description": "Утюг", "image": "", "category": category, "purchase_price": 2000}
        ]

        for product in products:
            #ПРОХОДИМСЯ ПО КАЖДОМУ СПИСКУ И ЗАПИСЫВАЕМ ПРОДУКТ
            product, created = Products.objects.get_or_create(**product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added book: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Book already exists: {product.name}'))
