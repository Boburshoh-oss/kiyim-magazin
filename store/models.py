from email.policy import default
from unicodedata import category
from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    title           = models.CharField(max_length=200,unique=True)
    slug            = models.SlugField(blank=True,unique=True)
    description     = models.TextField(blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey("category.Category",on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[self.category.slug,self.slug])
    
    def __str__(self) -> str:
        return self.title

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category=VARIATION_CATEGORY_CHOICE.COLOR, is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category=VARIATION_CATEGORY_CHOICE.SIZE,is_active=True)

class VARIATION_CATEGORY_CHOICE(models.TextChoices):
        COLOR = "color", "color"
        SIZE = 'size', 'size'
        
class Variation(models.Model):
    product             = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100,choices=VARIATION_CATEGORY_CHOICE.choices)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    
    objects = VariationManager()
    
    def __str__(self) -> str:
        return f"{self.product} > {self.variation_category} > {self.variation_value}"