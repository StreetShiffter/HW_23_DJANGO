from django.contrib import admin
from django.contrib.admin.utils import help_text_for_field

from catalog.models import Category, Products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)



@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purchase_price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)
