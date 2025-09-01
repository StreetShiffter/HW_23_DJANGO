from .models import Products

def get_products_by_category(category_id):
    """
    Возвращает QuerySet продуктов в указанной категории.
    Только опубликованные.
    """
    if not category_id:
        return Products.objects.none()

    return Products.objects.filter(category_id=category_id, is_published=True)