from django.contrib import admin
from .models import *
# Register your models here.


class ViewProduct(admin.ModelAdmin):
    empty_value_display = 'Trống'
    list_display = ("name_product", "created_by", "price", "created_at", "slug_product")
    fields = ("name_product", "created_by", "describe", "content", "main_picture", "category", "price", "discount", "num_available")


admin.site.register(Products, ViewProduct)
admin.site.register(Category)
admin.site.register(ProductPictures)
