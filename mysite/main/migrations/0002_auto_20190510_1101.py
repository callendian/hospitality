# Generated by Django 2.2 on 2019-05-10 18:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('country_code', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='guide',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 10, 11, 1, 54, 270331), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 10, 11, 1, 54, 272330), verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='tours',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 10, 11, 1, 54, 271328), verbose_name='date created'),
        ),
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=22, verbose_name='name')),
                ('description', models.CharField(max_length=250, verbose_name='description')),
                ('createdAt', models.DateTimeField(default=datetime.datetime(2019, 5, 10, 11, 1, 54, 276326), verbose_name='date created')),
                ('editedAt', models.DateTimeField(null=True, verbose_name='date edited')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tour', models.ManyToManyField(to='main.Tours')),
            ],
        ),
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('state_code', models.CharField(max_length=5, null=True)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Countries')),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('city_code', models.CharField(max_length=5, null=True)),
                ('state_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.States')),
            ],
        ),
    ]