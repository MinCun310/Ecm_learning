from rest_framework import serializers

from .models import Category, Brand, Product, ProductLine

class CategorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class BrandSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

class ProductLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    class Meta:
        model = ProductLine
        exclude = ['id', 'product', 'is_active']
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    brand_name = serializers.CharField(source='brand.name')
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['category', 'brand']