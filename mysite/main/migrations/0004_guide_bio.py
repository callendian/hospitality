# Generated by Django 2.2 on 2019-05-28 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_savedtour'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]