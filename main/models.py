from django.db import models
from django.contrib.auth.models import User


class Information(models.Model):
    logo = models.ImageField()
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    tw = models.URLField()
    tg = models.URLField()
    fb = models.URLField()
    insta = models.URLField()
    map = models.TextField()

    def __str__(self):
        return self.phone


class Service(models.Model):
    logo = models.ImageField()
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    bg = models.ImageField()
    url = models.URLField()

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='team/')
    tw = models.URLField()
    tg = models.URLField()
    fb = models.URLField()
    insta = models.URLField()


class Category(models.Model):
    name = models.CharField(max_length=255)


class ProductPhoto(models.Model):
    photo = models.ImageField(upload_to='Product/')


class Tag(models.Model):
    name = models.CharField(max_length=255)


class ProductInfo(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Brand(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    photo = models.ManyToManyField(ProductPhoto)
    in_slider = models.BooleanField(default=False)
    in_ad = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    bonus_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    bonus_percent = models.FloatField(default=0)
    sale = models.BooleanField(default=True)
    rating = models.IntegerField()
    tag = models.ManyToManyField(Tag)
    info = models.ManyToManyField(ProductInfo)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    description = models.TextField()
    bonus_duration = models.DurationField(default=0)
    bonus_start = models.DateTimeField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Ad(models.Model):
    bg_photo = models.ImageField()
    text = models.CharField(max_length=255)


class Feedback(models.Model):
    photo = models.ImageField(upload_to='media/feedback/')
    name = models.CharField(max_length=255)
    text = models.TextField()


class Partner(models.Model):
    photo = models.ImageField(upload_to='Partner/')


class Blog(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateField()
    photo = models.ImageField(upload_to='blog/')


class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
