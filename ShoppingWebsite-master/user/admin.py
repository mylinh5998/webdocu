from django.contrib import admin
from . import models
# Register your models here.


class ViewUser(admin.ModelAdmin):
    empty_value_display = 'Trống'
    list_display = ("username", "get_full_name", "email", "phone")


admin.site.register(models.MyUser, ViewUser)