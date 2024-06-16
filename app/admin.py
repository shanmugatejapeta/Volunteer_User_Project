from django.contrib import admin
from .models import  Problems, Volunteers,VUser


from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')

# Unregister the original User admin
admin.site.unregister(User)

# Register the custom User admin
admin.site.register(User, UserAdmin)

# Register your models here.

admin.site.register(Problems)
admin.site.register(Volunteers)
admin.site.register(VUser)