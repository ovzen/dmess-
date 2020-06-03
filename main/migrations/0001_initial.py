# Generated by Django 3.0.5 on 2020-05-30 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=2000)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('image_url', models.CharField(default=False, max_length=200, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Dialog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('avatar', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='avatars', width_field='width_field')),
                ('width_field', models.IntegerField(default=0)),
                ('height_field', models.IntegerField(default=0)),
                ('bio', models.CharField(default="Hey there! I'm using dmess", max_length=70)),
                ('is_online', models.BooleanField(default=False)),
                ('last_online', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='WikiPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='wiki')),
                ('text_markdown', models.TextField(max_length=2000)),
                ('text_html', models.TextField(blank=True, max_length=2000)),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Dialog')),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'contact')},
            },
        ),
    ]
