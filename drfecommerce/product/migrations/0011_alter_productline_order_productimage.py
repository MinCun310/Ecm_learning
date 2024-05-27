# Generated by Django 4.1.4 on 2024-05-08 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_productline_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productline',
            name='order',
            field=models.PositiveIntegerField(blank=True, unique=True),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('alternative_text', models.CharField(max_length=100)),
                ('url', models.ImageField(default='test.jpg', upload_to=None)),
                ('order', models.PositiveIntegerField(blank=True, unique=True)),
                ('product_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='product.productline')),
            ],
        ),
    ]