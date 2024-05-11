from django.contrib import admin

from .models import Category, Product, Brand, ProductLine, ProductImage
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Product, Brand, ProductLine

# Register your models here.

class ProductLineInLine(admin.TabularInline):
    model = ProductLine

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInLine]

class ProductImageInLine(admin.TabularInline):
    model = ProductImage

class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine)
