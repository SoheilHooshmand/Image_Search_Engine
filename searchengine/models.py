from django.db import models

class Image(models.Model):
    url = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

class Color(models.Model):
    hex_code = models.CharField(max_length=7)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hex_code

class Size(models.Model):
    size = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.size

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField(Image, related_name='products')
    code = models.CharField(max_length=50)
    brand_id = models.IntegerField(null=True, blank=True)
    brand_name = models.CharField(max_length=255, null=True, blank=True)
    category_id = models.IntegerField(null=True, blank=True)
    category_name = models.CharField(max_length=255, null=True, blank=True)
    gender_id = models.IntegerField(null=True, blank=True)
    gender_name = models.CharField(max_length=255, null=True, blank=True)
    shop_id = models.IntegerField()
    shop_name = models.CharField(max_length=255)
    link = models.URLField()
    status = models.CharField(max_length=50)
    colors = models.ManyToManyField(Color, related_name='products')
    sizes = models.ManyToManyField(Size, related_name='products')
    region = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    off_percent = models.IntegerField()
    update_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
