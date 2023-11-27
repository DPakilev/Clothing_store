from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):

    CHOICES_COLOR = (
        ('Black', 'Черный'),
        ('Red', 'Красный'),
        ('Grey', 'Серый'),
        ('Green', 'Зеленый'),
        ('Yellow', 'Желтый'),
        ('Pink', 'Розовый'),
        ('White', 'Белый'),
    )

    CHOICES_COUNTRY = (
        ('RU', 'Россия'),
        ('US', 'США'),
        ('FR', 'Франция'),
        ('IT', 'Италия'),
        ('TU', 'Турция'),
        ('CN', 'Китай'),
    )

    CHOICES_SIZE = (
        ('40', '40'),
        ('42', '42'),
        ('44', '46'),
        ('46', '46'),
        ('48', '48'),
        ('50', '50'),
        ('52', '52'),
    )

    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=255)
    Image = models.ImageField(upload_to='')
    id = models.AutoField(primary_key =True)
    price = models.PositiveIntegerField()
    country = models.CharField(max_length=2, choices=CHOICES_COUNTRY)
    composition = models.CharField(max_length=50)
    color = models.CharField(max_length=10, choices=CHOICES_COLOR)
    size = models.IntegerField(choices=CHOICES_SIZE)
    category = models.ManyToManyField(Category, through='ProductCategory')

    def get_absolut_url(self):
        return f'/product/{self.id}'

    def __str__(self):
        return f'{self.name}'


class Customer(models.Model):

    CHOICES = (
        ('M', 'Мужчина'),
        ('W', 'Женщина'),
        ('S', 'Секрет')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField(default=89999999999)
    gender = models.CharField(choices=CHOICES)
    birthday = models.DateField()
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}'


class ShoppingBasket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} в корзине у {self.user.username}'


class Favorites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} в избранном у {self.user.username}'


class ProductCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} - {self.product.name}'


class Review(models.Model):

    CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    evaluation = models.CharField(choices=CHOICES)
    description = models.TextField(max_length=500)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.evaluation} к товару {self.product}'

    def get_absolut_url(self, *args, **kwargs):
        return f'/product/{self.product.id}'
