# Generated by Django 3.2.8 on 2021-11-06 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='inventory_id',
            new_name='inventory',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='seller_id',
            new_name='seller',
        ),
    ]
