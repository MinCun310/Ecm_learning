from rest_framework import serializers

from .models import Category, Brand, Product, ProductLine, ProductImage, Attribute, AttributeValue, ProductType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['name', 'alternative_text', 'order', 'image_url']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['name', 'id']


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name')
    description_attribute = serializers.CharField(source='attribute.description')

    class Meta:
        model = AttributeValue
        fields = ['attribute_name', 'att_value', 'description_attribute']


class ProductLineSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        exclude = ['id', 'product', 'is_active']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop('attribute_value')
        attr_values = {}
        for key in av_data:
            attr_values.update({key['attribute_name']: key['att_value']})
        data.update({'attribute_value': attr_values})
        return data


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    # brand_name = serializers.CharField(source='brand.name')
    product_line = ProductLineSerializer(many=True)
    product_type_attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['category', 'brand']

    def get_product_type_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attribute__product_type__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop('product_type_attribute')
        attr_values = {}
        for key in av_data:
            attr_values.update({key['id']: key['name']})
        data.update({'product_type_attribute': attr_values})
        return data
