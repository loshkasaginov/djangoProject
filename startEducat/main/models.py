from django.db import models
from django.urls import reverse


class Product_manufacturer(models.Model):
    class Meta:
        db_table = "product_manufacturer"
        verbose_name = "производитель"
        verbose_name_plural = "производители"

    product_manufacturer = models.CharField(max_length=100, help_text="Enter manufacturer name",
                                            verbose_name="производитель")
    time_manufacturer_created = models.DateField(auto_now_add=True, verbose_name="время создания записи")

    def __str__(self):
        return f'{self.product_manufacturer}'

    def get_absolute_url(self):
        return reverse('product_manufacturer-detail', args=[str(self.id)])


class Product(models.Model):
    class Meta:
        db_table = "product"
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    product_name = models.CharField(max_length=100, help_text="Enter product name", verbose_name="продукт")
    product_description = models.TextField(help_text="Enter cpu description", verbose_name="описание продукта")
    product_manufacturer = models.ForeignKey('product_manufacturer', on_delete=models.CASCADE,
                                             verbose_name="внешняя ссылка на производителя")
    product_price = models.IntegerField(verbose_name="цена")
    time_product_created = models.DateField(auto_now_add=True, verbose_name="время создания записи")
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.product_name, self.product_manufacturer, self.product_price, self.time_product_created}'
