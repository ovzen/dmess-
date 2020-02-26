from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Dialog

from main.models import Status, UserSetting


class UserSettingInline(admin.StackedInline):
    model = UserSetting
    can_delete = False


class UserSettingAdmin(UserAdmin):
    inlines = (UserSettingInline, )


# Register your models here.
admin.site.unregister(User)
admin.site.register(Status)
admin.site.register(Dialog)
admin.site.register(User, UserSettingAdmin)
# admin.site.register(Author)
