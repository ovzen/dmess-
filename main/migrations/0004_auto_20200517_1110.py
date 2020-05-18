# Generated by Django 3.0.5 on 2020-05-17 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_merge_20200517_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dialog',
            name='admin_only',
        ),
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_online',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='dialog',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
