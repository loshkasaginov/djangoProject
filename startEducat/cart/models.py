from django.db import models
from django.contrib.auth.models import User
from main.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"

    def get_total_price(self):
        return self.product.product_price * self.quantity
