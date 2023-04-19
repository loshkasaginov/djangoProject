from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product_manufacturer, Product
from .models import Review


class ProductmanufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_manufacturer', 'time_manufacturer_created')


class ProductAdmin(admin.ModelAdmin):
    # Ваши существующие настройки, если есть
    list_display = (
    'id', 'product_name', 'product_manufacturer', 'product_price', 'product_image', 'time_product_created')
    # Добавьте поле cpuImage в fields
    fields = ['product_name', 'product_description', 'product_manufacturer', 'product_price', 'product_image']


admin.site.register(Product_manufacturer, ProductmanufacturerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)

# "/"
# "/about"
# "/products/cpu"
# "/products/manufacturer"
# "/products/cpu/<id>"
# "/products/manufacturer/<id>"
