# Generated by Django 2.2 on 2019-06-06 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190605_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
