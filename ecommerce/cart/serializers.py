from rest_framework import serializers
from cart.models import Cart

from cart.models import Order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','product','quantity','user']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields=['id','product','user','no_of_items','address','phone','order_status','delivery_status','ordered_date']

