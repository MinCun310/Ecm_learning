from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import Category, Brand, Product
from .serializers import CategorySerialzier, BrandSerialzier, ProductSerializer


# Create your views here.
class CategoryView(APIView):
    @extend_schema(responses=CategorySerialzier)
    def get(self, request):
        instance = Category.objects.all()
        serializer = CategorySerialzier(instance=instance, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Fetched category successfully'
        })

class BrandView(APIView):
    @extend_schema(responses=BrandSerialzier)
    def get(self, request):
        instance = Brand.objects.all()
        serializer = BrandSerialzier(instance=instance, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Fetched brand successfully'
        })

    def delete(self, request):
        print('delete......')
        param_brand_name = request.query_params.get('brand_name')
        brand = Brand.objects.filter(name=param_brand_name)
        brand.delete()
        return Response({
            'message': f'Brand {param_brand_name} deleted successfully'
        })

class ProductView(APIView):
    @extend_schema(responses=ProductSerializer)
    def get(self, request):
        product = Product.objects_active_manager.isactive()
        param_category_name = request.query_params.get('category_name')
        param_slug = request.query_params.get('slug')

        if param_category_name:
            product_filter = product.filter(category__name=param_category_name)
            if product_filter.exists():
                serializer = ProductSerializer(instance=product_filter, many=True)
                return Response({
                    'data': serializer.data,
                    'message': 'The product of category name is fetched successfully'
                })
            return Response({
                'message': f'The product {param_category_name} cannot found with category name'
            })
        elif param_slug:
            try:
                product_get_slug = product.get(slug=param_slug)
                serializer = ProductSerializer(instance=product_get_slug)
                return Response({
                    'data': serializer.data,
                    'message': 'The product slug is fetched successfully'
                })
            except Product.DoesNotExist:
                return Response({
                    'message': f'The product {param_slug} cannot found with slug'
                })
        else:
            if product.exists():
                serializer = ProductSerializer(instance=product, many=True)
                return Response({
                    'data': serializer.data,
                    'message': 'Fetched product successfully'
                })
            else:
                return Response({
                    'message': 'No product found'
                })

