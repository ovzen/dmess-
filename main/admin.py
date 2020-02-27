from django.contrib import admin
from .models import UserSetting, Friend, Status, Dialog, Message

# Register your models here.
admin.site.register(UserSetting)
admin.site.register(Friend)
admin.site.register(Status)
admin.site.register(Dialog)
admin.site.register(Message)
# admin.site.register(Author)
