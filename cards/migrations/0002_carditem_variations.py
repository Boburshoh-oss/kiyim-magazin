# Generated by Django 4.0 on 2022-03-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carditem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]
