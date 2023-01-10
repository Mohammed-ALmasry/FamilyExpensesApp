from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .models import CustomeUser,family,Material,outlayType,outlay

class CustomeUserAdmin(UserAdmin): 
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'user_type','is_head'
        )
    pass

admin.site.register(CustomeUser) 
admin.site.register(family) 
admin.site.register(Material)
admin.site.register(outlayType)
admin.site.register(outlay)