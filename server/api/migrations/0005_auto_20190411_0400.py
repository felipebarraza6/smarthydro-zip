# Generated by Django 2.1.4 on 2019-04-11 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190411_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='nombre',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]