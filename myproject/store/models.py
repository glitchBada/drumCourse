from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="название категории")
    slug = models.SlugField(unique=True, help_text="Unique URL identifier", verbose_name="уникальный идентификатор URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    class Meta:
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="название бренда")
    slug = models.SlugField(unique=True, verbose_name="уникальный идентификатор URL")
    logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True, verbose_name="логотип бренда")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="название продукта")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="категория продукта")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="бренд продукта")
    description = models.TextField(blank=True, verbose_name="описание продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена продукта")
    slug = models.SlugField(unique=True, help_text="Unique URL identifier", verbose_name="уникальный идентификатор URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата обновления")

    class Meta:
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="продукт")
    image = models.ImageField(upload_to='product_images/', verbose_name="изображение продукта")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Image description", verbose_name="описание изображения")

    def __str__(self):
        return f"Image for {self.product.name}"
    
    class Meta:
        verbose_name_plural = "Изображения продуктов"
        
