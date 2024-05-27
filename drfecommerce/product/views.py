from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.db.models import Prefetch

from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .models import Category, Brand, Product, ProductLine
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer, ProductLineSerializer


# Create your views here.

class CategoryView(APIView):
    @extend_schema(responses=CategorySerializer)
    def get(self, request):
        instance = Category.objects_active_manager.all()
        serializer = CategorySerializer(instance=instance, many=True)
        return Response({
            'data': serializer.data,
            'message': 'Fetched category successfully'
        })


class BrandView(APIView):
    @extend_schema(responses=BrandSerializer)
    def get(self, request):
        instance = Brand.objects.all()
        serializer = BrandSerializer(instance=instance, many=True)
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
        product = Product.objects_active_manager.all()

        # sắp xếp theo order của ProductLine
        product = product.prefetch_related(
            Prefetch('product_line', queryset=ProductLine.objects_active_manager.order_by('order')))

        param_category_name = request.query_params.get('category_name')
        param_slug = request.query_params.get('slug')
        param_product = request.query_params.get('product')

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
        elif param_product:
            try:
                product_get_name = product.filter(name=param_product)
                serializer = ProductSerializer(instance=product_get_name)
                return Response({
                    'data': serializer.data,
                    'message': 'The product name is fetched successfully'
                })
            except Product.DoesNotExist:
                return Response({
                    'message': f'The product {param_product} cannot found with name'
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
