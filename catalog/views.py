from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View
from django.urls import reverse, reverse_lazy
from catalog.forms import ProductsForm
from catalog.models import Products, Category
from .services import get_products_by_category  # ← импорт из services.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

class ProductsByCategoryView(ListView):
    model = Products
    context_object_name = 'products'
    template_name = 'catalog/products_by_category.html'

    def get_queryset(self):
        self.category = Category.objects.get(pk=self.kwargs['category_id'])# ← получаем все id категорий
        return get_products_by_category(self.category.id)# ← Получаем товары по категории

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст:
        - current_category: текущую категорию (для заголовка)
        - category: все категории (для отображения в меню)
        """
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        context['category'] = Category.objects.exclude(id__isnull=True).all()
        return context


class HomeListView(ListView):
    '''Главная страница'''
    model = Products
    context_object_name = 'products'  # ← сейчас это object_list будет в 'product'
    template_name = 'catalog/home.html'


#Для низкоуровневого кэширования по времени(lambda - проверка есть кэш или пуст. Если пуст, то делает запрос.)
    def get_queryset(self):
        '''Достаем данные из БД и кэшируем'''
        if self.request.user.is_authenticated and self.request.user.has_perm('catalog.can_unpublish_product'):
            cache_key = 'home_view_all_products'# Ключ кэша
            queryset = Products.objects.all()# модератор видит всё (объект кэша)
        else:
            cache_key = 'home_view_published_only'
            queryset = Products.objects.filter(is_published=True)# остальные — только опубликованные

        return cache.get_or_set(cache_key, queryset, 60)#метод(ключ, объект, время в секундах)

    def get_context_data(self, **kwargs):
        '''Отображение данных в шаблоне'''
        context = super().get_context_data(**kwargs)
        context['category'] = cache.get_or_set('category_list',lambda: Category.objects.exclude(id__isnull=True),60)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm

    # fields = '__all__' # спец метод для добавления всех полей разом

    def form_valid(self, form):
        # Устанавливаем владельца перед сохранением
        # form.instance - объект формы не сохраненный в БД, .owner - поле с ForeginKey
        form.instance.owner = self.request.user
        return super().form_valid(form)  # Сохранение и редирект на get_success_url

    def get_success_url(self):
        return reverse('catalog:product', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Products
    form_class = ProductsForm

    def test_func(self):
        '''test_func - особый метод проверки UserPassesTestMixin'''
        # Проверяем: пользователь — владелец ИЛИ имеет право на удаление
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.delete_products')

    # Если нет прав — 403 Forbidden
    raise_exception = True

    def get_success_url(self):
        '''Перенаправление по запросу'''
        return reverse('catalog:product', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        '''Проверка post запроса на публикацию'''
        self.object = self.get_object()

        # 🔥 Если пришёл POST с флагом toggle_publish — просто переключаем статус
        if 'toggle_publish' in request.POST:
            if not request.user.has_perm('catalog.can_unpublish_product'):
                return HttpResponseForbidden("У вас нет прав на публикацию")

            self.object.is_published = not self.object.is_published
            self.object.save()
            return redirect(self.get_success_url())

        # ⬇️ Иначе — обычное поведение (редактирование формы)
        return super().post(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''Удаляет продукт и проверяет право конкретного авторизированного пользователя через UserPassesTestMixin'''
    model = Products
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    # # Указываем требуемое разрешение для проверки права у пользователя конкретного
    # permission_required = 'catalog.delete_products'

    def test_func(self):
        '''test_func - особый метод проверки UserPassesTestMixin'''
        # Проверяем: пользователь — владелец ИЛИ имеет право на удаление
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.delete_products')

    # Если нет прав — 403 Forbidden
    raise_exception = True

# @method_decorator(cache_page(60 * 15), name='dispatch') - кэширование страницы через контроллер
class ProductDetailView(DetailView):
    '''Загрузка страницы с конкретным продуктом по первичному ключу'''
    model = Products
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.exclude(id__isnull=True).all()
        return context


class FeedbackView(View):
    template_name = 'catalog/contacts.html'  # Нужно прописать genm, т.к. нету действия view.

    def get(self, request):
        # При GET-запросе просто показываем шаблон
        return render(request, self.template_name)

    def post(self, request):
        # При POST — забираем данные вручную
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Обрабатываем и отвечаем
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.exclude(id__isnull=True).all()
        return context
