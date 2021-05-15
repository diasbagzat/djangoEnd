from django.db import models
from auth_.models import User

# Create your models here.

class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('category_name')

class Category(models.Model):

    category_name = models.CharField(max_length=100)
    objects = CategoryManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name


class ProductManager(models.Manager):
    def get_by_category_without_relation(self, category_name):
        return self.filter(category=category_name)


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Наименование")
    image = models.ImageField(verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = 'Товар'
        ordering = ('title', 'price')

    def __str__(self):
        return self.title


class Cart(models.Model):
    items = models.ManyToManyField(Product)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Корзина'


class Order(models.Model):
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")
    address = models.CharField(max_length=255, verbose_name='Адрес')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)


    class Meta:
        verbose_name='Заказ'

