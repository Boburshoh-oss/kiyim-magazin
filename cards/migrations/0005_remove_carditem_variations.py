# Generated by Django 4.0 on 2022-04-04 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_alter_carditem_variations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carditem',
            name='variations',
        ),
    ]
