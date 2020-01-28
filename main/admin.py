from django.contrib import admin
from .models import Dialog

from main.models import Status

# Register your models here.
admin.site.register(Status)
admin.site.register(Dialog)
# admin.site.register(Author)
