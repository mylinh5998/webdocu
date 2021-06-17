# Generated by Django 3.0.4 on 2020-03-24 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20200318_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=15, null=True, unique=True),
        ),
    ]
