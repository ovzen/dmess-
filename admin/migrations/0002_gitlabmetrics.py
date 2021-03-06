# Generated by Django 3.0.5 on 2020-05-04 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitlabMetrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fetch_date', models.DateTimeField(auto_now_add=True)),
                ('opened_issues', models.IntegerField()),
                ('opened_merge_requests', models.IntegerField()),
                ('current_branches', models.IntegerField()),
                ('commits', models.IntegerField()),
            ],
        ),
    ]
