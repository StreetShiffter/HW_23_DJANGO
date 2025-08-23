from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=300, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class Products(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length = 300, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE,
                                 related_name='products',
                                 verbose_name="Категория",
                                 null=True,
                                 blank=True)
    purchase_price = models.IntegerField(verbose_name='Цена за покупку')
    owner = models.ForeignKey(User,
                              on_delete = models.CASCADE,
                              related_name='owned_products',
                              verbose_name='Продукт пользователя')
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Указывает, опубликован ли товар на сайте. По умолчанию — не опубликован.",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.name} {self.purchase_price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name', 'purchase_price']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]
