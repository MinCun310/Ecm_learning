# Generated by Django 4.1.4 on 2024-05-09 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_alter_productimage_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='url',
            field=models.ImageField(blank=True, null=True, upload_to='product_image'),
        ),
    ]