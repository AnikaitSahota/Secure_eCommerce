# Generated by Django 3.2.8 on 2021-11-08 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20211107_0317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='SKU',
        ),
    ]
