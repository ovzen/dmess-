# Generated by Django 3.0.5 on 2020-04-27 20:39

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200427_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialog',
            name='user_dictionary',
            field=picklefield.fields.PickledObjectField(default=None, editable=False),
        ),
    ]
