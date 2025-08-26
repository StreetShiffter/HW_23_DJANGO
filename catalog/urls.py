from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from .views import HomeListView, ProductDetailView, FeedbackView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name="product"),
    path('contacts/',FeedbackView.as_view(), name="contacts"),
    path('', HomeListView.as_view(), name="home"),
    path('product/create/', ProductCreateView.as_view(), name="create"),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name="update"),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name="delete"),
]