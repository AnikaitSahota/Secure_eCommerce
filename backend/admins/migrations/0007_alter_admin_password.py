# Generated by Django 3.2.8 on 2021-11-07 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0006_auto_20211108_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]