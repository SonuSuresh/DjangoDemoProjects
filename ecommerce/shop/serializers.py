from django.contrib.auth.models import User
from rest_framework import serializers
from shop.models import Category

from shop.models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','desc','image']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','desc','image','price','stock']

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['id','username','password']

    def create(self, validated_data):
        u=User.objects.create_user(username=validated_data['username'],password=validated_data['password'])
        u.save()
        return u

