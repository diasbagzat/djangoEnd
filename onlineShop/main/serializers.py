from rest_framework import serializers
from .models import Product, Cart, Category, Order

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category_name = serializers.CharField()

    def create(self, validated_data):

        productCategory = Category.objects.create(category_name=validated_data.get('category_name'))
        return productCategory

    def update(self, instance, validated_data):
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.save()
        return instance

    def validate(self, data):
        if data['categoryName'] == '':
            raise serializers.ValidationError("Empty Category Name")
        return data

class ProductSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    description = serializers.CharField(max_length=255)
    category = CategorySerializer()

    def create(self, validated_data):
        category = Category.objects.get(id=validated_data.get('category'))
        product = Product.objects.create(title=validated_data.get('title'),
                                         price=validated_data.get('price'),
                                         description=validated_data.get('description'),
                                         category=category)
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance

    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price can't be negative number or zero!")
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

