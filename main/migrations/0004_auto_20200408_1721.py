# Generated by Django 3.0 on 2020-04-08 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200408_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipage',
            name='text_html',
            field=models.TextField(blank=True, max_length=2000),
        ),
    ]