from django.contrib import admin
from .models import Category, Product, Brand, ProductLine, ProductImage, AttributeValue, Attribute, ProductType
from django.urls import reverse

from django.utils.safestring import mark_safe
from django.utils.html import format_html


from .models import Category, Product, Brand, ProductLine, ProductImage
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Product, Brand, ProductLine

# Register your models here.

class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


class ProductImageInLine(admin.TabularInline):
    model = ProductImage


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue.product_line_attribute_value.through


class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine, AttributeValueInline]


class AttributeInline(admin.TabularInline):
    model = Attribute.product_type_attribute.through


class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]


class ProductImageInLine(admin.TabularInline):
    model = ProductImage

class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine]

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductType, ProductTypeAdmin)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_url']
    fieldsets = (
        ('Product Image', {
            'fields': (
                'name', 'alternative_text', 'product_line', "order", "url", "image_tag")
        }),)
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        return format_html('<img width="200px" src="{}" />'.format(obj.url.url))

    image_tag.short_description = 'Image'

    def image_url(self, obj):
        return mark_safe(f'<img src={obj.url.url} width="50" height="50" />')
