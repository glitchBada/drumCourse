from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product-detail'),
    path('apply/', views.ApplicationView.as_view(), name='application'),
    path('brands/', views.BrandList.as_view(), name='brand-list'),
    path('new-products/', views.NewProductsList.as_view(), name='new-products'),
]