from rest_framework import serializers
from products.models import Product, Bar


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('factory_company',)


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        exclude = ('freight', )

    def validate(self, attrs):
        product_id = attrs['product'].id
        amount = attrs['amount']
        product = Product.objects.get(pk=product_id)
        product_amount = product.amount
        if amount > product_amount or product_amount == 0:
            raise serializers.ValidationError({
                "amount": "The volume of the ordered data load is greater than the allowed amount"
            })
        return attrs
