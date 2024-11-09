from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """ Category Model """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):    
        return self.friendly_name


class SubCategory(models.Model):
    """ Sub category model """
    category_id = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return self.name
    
    def get_friendly_name(self):    
        return self.friendly_name


class Product(models.Model):
    """ Products Model """
    category_id = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    subcategory_id = models.ForeignKey(
        'SubCategory', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_clearance = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name