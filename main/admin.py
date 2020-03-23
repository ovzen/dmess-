from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from main.models import UserProfile, Dialog, Message, Contact


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)


# Register your models here.
admin.site.unregister(User)
admin.site.register(Dialog)
admin.site.register(User, UserProfileAdmin)
admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Message)
