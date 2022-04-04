from distutils.command.upload import upload
from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True)
    cat_img = models.ImageField(upload_to='photos/categories/',blank=True)
    
    def get_absolute_url(self):
        return reverse("detail_category", args=[self.slug])
    
    
    def __str__(self):
        return self.title