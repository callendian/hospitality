# Generated by Django 2.2 on 2019-05-12 08:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20190512_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 12, 8, 13, 47, 441984), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 12, 8, 13, 47, 443193), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='tours',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 12, 8, 13, 47, 442580), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='visitors',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 12, 8, 13, 47, 444883), verbose_name='date created'),
        ),
    ]
