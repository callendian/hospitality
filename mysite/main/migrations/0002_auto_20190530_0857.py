# Generated by Django 2.2 on 2019-05-30 15:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitors',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 30, 8, 57, 24, 92421), verbose_name='date created'),
        ),
    ]