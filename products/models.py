from django.db import models
from accounts.models import User
import string
import random
from .utils import generate_text


class Product(models.Model):
    STATUS = (
        ('close', 'Close'),
        ('open', 'Open')
    )
    factory_company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    postage_date = models.DateField()
    status = models.CharField(max_length=5, choices=STATUS, default='open')

    def __str__(self):
        return self.title


class Bar(models.Model):
    STATUS = (
        ('waiting', 'Waiting for confirmation'),
        ('valid', 'Valid')
    )
    barcode = models.CharField(max_length=50, null=True, unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bars_product')
    freight = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bars_freight')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bars_driver')
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='waiting')

    def save(self, *args, **kwargs):
        if not self.barcode:
            self.barcode = generate_text(20)

        # TODO:خط های زیر باید در یک تابع دیگر نوشته شود ، رعایت اصول صالید
        # total_amount_remaining, order_amount = self.product.amount, self.amount
        # if order_amount == total_amount_remaining:
        #     self.product.amount = 0
        # elif order_amount < total_amount_remaining:
        #     self.product.amount -= self.amount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.barcode
