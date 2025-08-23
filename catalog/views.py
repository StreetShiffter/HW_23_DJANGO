from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.template.context_processors import request
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View
from django.urls import reverse, reverse_lazy

from catalog.forms import ProductsForm
from catalog.models import Products, Category
from users.models import User


class HomeListView(ListView):
    '''Главная страница'''
    model = Products
    context_object_name = 'products'  # ← сейчас это object_list будет в 'product'
    template_name = 'catalog/home.html'

    def get_queryset(self):
        """Фильтруем: только опубликованные для обычных, все — для модераторов"""
        if self.request.user.has_perm('catalog.can_unpublish_product'):
            return Products.objects.all()  # модератор видит всё
        else:
            return Products.objects.filter(is_published=True)  # остальные — только опубликованные

    def get_context_data(self, **kwargs):
        '''Подгружаем данные с БД'''
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm
    # fields = '__all__' # спец метод для добавления всех полей разом

    def get_success_url(self):
        return reverse('catalog:product', kwargs={'pk': self.object.pk})



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    form_class = ProductsForm

    def get_success_url(self):
        return reverse('catalog:product', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
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



class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Products
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    # Указываем требуемое разрешение
    permission_required = 'catalog.delete_products'

    # Если нет прав — 403 Forbidden
    raise_exception = True




class ProductDetailView(DetailView):
    '''Загрузка страницы с конкретным продуктом по первичному ключу'''
    model = Products
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        '''Метод распаковки моделей'''
        context = super().get_context_data(**kwargs)
        context['products'] = Products.objects.all()
        context['category'] = Category.objects.all()
        return context


class FeedbackView(View):
    template_name = 'catalog/contacts.html'# Нужно прописать genm, т.к. нету действия view.

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


