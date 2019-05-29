# Generated by Django 2.2 on 2019-05-29 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_guide_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='title',
            field=models.CharField(default='Tour', max_length=50),
        ),
        migrations.AlterField(
            model_name='tourreview',
            name='booking',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Booking'),
        ),
    ]
