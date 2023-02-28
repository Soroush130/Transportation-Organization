from django.contrib import admin
from .models import Product, Bar


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'factory_company', 'status']


class BarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Bar, BarAdmin)
