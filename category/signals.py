from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.dispatch import receiver
from .utils import get_unique_slug
from .models import Category

# def slugify_pre_save(sender,instance,*args,**kwargs):
#     title = instance.title
#     slug = instance.slug
#     if slug is None:
#         instance.slug = slugify(title)

def unique_slugify_pre_save(sender,instance,*args,**kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = get_unique_slug(instance,size=5)

pre_save.connect(unique_slugify_pre_save,sender=Category)