# Generated by Django 3.2.8 on 2021-11-07 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20211107_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email_id',
            field=models.CharField(default='random_email@random.com', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer_otp',
            name='meta_data',
            field=models.CharField(default='NULL', max_length=500),
            preserve_default=False,
        ),
    ]
