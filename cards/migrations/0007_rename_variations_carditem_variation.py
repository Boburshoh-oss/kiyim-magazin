# Generated by Django 4.0 on 2022-04-04 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_carditem_variations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carditem',
            old_name='variations',
            new_name='variation',
        ),
    ]
