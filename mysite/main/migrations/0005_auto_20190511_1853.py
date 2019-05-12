# Generated by Django 2.2 on 2019-05-11 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190511_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guide',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 18, 53, 42, 605969), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 18, 53, 42, 607304), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tours',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 18, 53, 42, 606623), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='visitors',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 18, 53, 42, 609167), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='visitors',
            name='description',
            field=models.CharField(max_length=250, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='visitors',
            name='name',
            field=models.CharField(max_length=22, verbose_name='name'),
        ),
    ]
