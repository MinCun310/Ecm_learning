from django.urls import path

from drfecommerce.product.views import CategoryView, BrandView, ProductView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('brand/', BrandView.as_view()),
    path('product/', ProductView.as_view()),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
