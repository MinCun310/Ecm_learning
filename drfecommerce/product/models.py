from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
import environ
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField

# Create your models here.

env = environ.Env()
environ.Env.read_env()


class ActiveManager(models.Manager):
    def isactive(self):
        return self.get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    # manage activation of product
    objects_active_manager = ActiveManager()

    # isactive = ActiveManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    # manage activation of product
    objects_active_manager = ActiveManager()

    # isactive = ActiveManager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    product_type = models.ForeignKey('ProductType', on_delete=models.PROTECT, related_name='product')

    # manage activation of product
    objects_active_manager = ActiveManager()

    # isactive = ActiveManager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    att_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='attribute_value')

    def __str__(self):
        return f'{self.attribute.name}-{self.att_value}'


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,
                                        related_name='product_line_attribute_value_av')
    product_line = models.ForeignKey('ProductLine', on_delete=models.CASCADE,
                                     related_name='product_line_attribute_value_pl')

    class Meta:
        unique_together = ('attribute_value', 'product_line')

    def clean(self):
        qs = ProductLineAttributeValue.objects.filter(
            attribute_value__attribute__name=self.attribute_value.attribute.name,
            product_line=self.product_line
        )
        for obj in qs:
            if self.id != obj.id and self.attribute_value.attribute.name == obj.attribute_value.attribute.name:
                raise ValidationError(f'Duplicate {self.attribute_value.attribute.name} name.')

        # qs = ProductLineAttributeValue.objects.filter(
        #     attribute_value=self.attribute_value, product_line=self.product_line).exists()
        # if not qs:
        #     iqs = Attribute.objects.filter(attribute_value__product_line_attribute_value=self.product_line).values_list('pk', flat=True)
        #     if self.attribute_value.attribute.pk in list(iqs):
        #         raise ValidationError(f'Duplicate {self.attribute_value.attribute.name} name.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLineAttributeValue, self).save(*args, **kwargs)


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    sku = models.CharField(max_length=100, null=True)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_line')
    is_active = models.BooleanField(default=False)
    order = OrderField(unique_for_field='product', blank=True)
    attribute_value = models.ManyToManyField(AttributeValue, through=ProductLineAttributeValue,
                                             related_name='product_line_attribute_value')

    # manage activation of product
    objects_active_manager = ActiveManager()

    # isactive = ActiveManager()

    def __str__(self):
        return str(self.order)

    def clean(self):
        qs = ProductLine.objects_active_manager.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)
        # if self.order is None:
        #     product_line = ProductLine.objects_active_manager.filter(product=self.product)
        #     max_order = product_line.aggregate(models.Max('order'))['order__max']
        #     if max_order is None:
        #         max_order = 0
        #         self.order = max_order + 1
        # #     self.order = max_order + 1
        # return super().save(*args, **kwargs)


class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to='product_image', null=True, blank=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_image')
    order = OrderField(unique_for_field='product_line', blank=True)

    # manage activation of product
    objects_active_manager = ActiveManager()

    # isactive = ActiveManager()

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return env('DOMAIN_SITE') + settings.MEDIA_URL + str(self.url)

    def clean(self):
        qs = ProductImage.objects_active_manager.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)
        # if self.order is None:
        #     product_image = ProductImage.objects.filter(product_line=self.product_line)
        #     max_order = product_image.aggregate(models.Max('order'))['order__max']
        #     if max_order is None:
        #         max_order = 0
        #         self.order = max_order + 1
        #     self.order = max_order + 1
        # return super().save(*args, **kwargs)


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    attribute = models.ManyToManyField(Attribute, through='ProductTypeAttribute', related_name='product_type_attribute')

    def __str__(self):
        return self.name


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='product_type_attribute_pt')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='product_type_attribute_a')

    class Meta:
        unique_together = ('product_type', 'attribute')

    def __str__(self):
        return f'{self.product_type}-{self.attribute}'

    def save(self, *args, **kwargs):
        if self.order is None:
            product_line = ProductLine.objects_active_manager.filter(product=self.product)
            max_order = product_line.aggregate(models.Max('order'))['order__max']
            print('check max order: ', max_order)
            if max_order is None:
                max_order = 0
                self.order = max_order + 1
            self.order = max_order + 1
        return super().save(*args, **kwargs)

      
class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to='product_image', null=True, blank=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_image')
    order = models.PositiveIntegerField(unique=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return env('DOMAIN_SITE') + settings.MEDIA_URL + str(self.url)

    def save(self, *args, **kwargs):
        if self.order is None:
            product_image = ProductImage.objects.filter(product_line=self.product_line)
            max_order = product_image.aggregate(models.Max('order'))['order__max']
            if max_order is None:
                max_order = 0
                self.order = max_order + 1
            self.order = max_order + 1
        return super().save(*args, **kwargs)
