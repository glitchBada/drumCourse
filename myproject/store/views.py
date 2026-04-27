from django.db.models import Q
from rest_framework import generics

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer


class NewProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('-created_at')[:10]


class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'brand').prefetch_related('images')
        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category__slug=category)
        if brand:
            queryset = queryset.filter(brand__slug=brand)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(category__name__icontains=search)
                | Q(brand__name__icontains=search)
            )
        return queryset


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('images')
    serializer_class = ProductSerializer
    lookup_field = 'slug'
