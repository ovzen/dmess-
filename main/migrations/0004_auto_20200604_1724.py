# Generated by Django 3.0.6 on 2020-06-04 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200604_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image_url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
