# Generated by Django 3.2.8 on 2021-11-07 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_auto_20211107_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_otp',
            name='meta_data',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
