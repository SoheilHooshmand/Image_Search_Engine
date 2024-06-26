from rest_framework import serializers
from .models import Product, Image, Color, Size


class ListOfStringsField(serializers.ListField):
    child = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    images = ListOfStringsField()
    colors = ListOfStringsField()
    sizes = ListOfStringsField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'images', 'code', 'brand_id', 'brand_name',
            'category_id', 'category_name', 'gender_id', 'gender_name', 'shop_id',
            'shop_name', 'link', 'status', 'colors', 'sizes', 'region', 'currency',
            'current_price', 'old_price', 'off_percent', 'update_date'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        colors_data = validated_data.pop('colors')
        sizes_data = validated_data.pop('sizes')

        product = Product.objects.create(**validated_data)

        for image_url in images_data:
            try:
                image = Image.objects.get(url=image_url)
            except Image.DoesNotExist:
                image = Image.objects.create(url=image_url)
            except Image.MultipleObjectsReturned:
                image = Image.objects.filter(url=image_url).first()

            product.images.add(image)

        for color_hex in colors_data:
            try:
                color = Color.objects.get(hex_code=color_hex)
            except Color.DoesNotExist:
                color = Color.objects.create(hex_code=color_hex)
            except Color.MultipleObjectsReturned:
                color = Color.objects.filter(hex_code=color_hex).first()

            product.colors.add(color)

        for size_value in sizes_data:
            try:
                size = Size.objects.get(size=size_value)
            except Size.DoesNotExist:
                size = Size.objects.create(size=size_value)
            except Size.MultipleObjectsReturned:
                size = Size.objects.filter(size=size_value).first()

            product.sizes.add(size)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        colors_data = validated_data.pop('colors', None)
        sizes_data = validated_data.pop('sizes', None)

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.code = validated_data.get('code', instance.code)
        instance.brand_id = validated_data.get('brand_id', instance.brand_id)
        instance.brand_name = validated_data.get('brand_name', instance.brand_name)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.category_name = validated_data.get('category_name', instance.category_name)
        instance.gender_id = validated_data.get('gender_id', instance.gender_id)
        instance.gender_name = validated_data.get('gender_name', instance.gender_name)
        instance.shop_id = validated_data.get('shop_id', instance.shop_id)
        instance.shop_name = validated_data.get('shop_name', instance.shop_name)
        instance.link = validated_data.get('link', instance.link)
        instance.status = validated_data.get('status', instance.status)
        instance.region = validated_data.get('region', instance.region)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.current_price = validated_data.get('current_price', instance.current_price)
        instance.old_price = validated_data.get('old_price', instance.old_price)
        instance.off_percent = validated_data.get('off_percent', instance.off_percent)
        instance.update_date = validated_data.get('update_date', instance.update_date)

        instance.save()

        if images_data:
            instance.images.clear()
            for image_url in images_data:
                try:
                    image = Image.objects.get(url=image_url)
                except Image.DoesNotExist:
                    image = Image.objects.create(url=image_url)
                except Image.MultipleObjectsReturned:
                    image = Image.objects.filter(url=image_url).first()
                instance.images.add(image)

        if colors_data:
            instance.colors.clear()
            for color_hex in colors_data:
                try:
                    color = Color.objects.get(hex_code=color_hex)
                except Color.DoesNotExist:
                    color = Color.objects.create(hex_code=color_hex)
                except Color.MultipleObjectsReturned:
                    color = Color.objects.filter(hex_code=color_hex).first()
                instance.colors.add(color)

        if sizes_data:
            instance.sizes.clear()
            for size_value in sizes_data:
                try:
                    size = Size.objects.get(size=size_value)
                except Size.DoesNotExist:
                    size = Size.objects.create(size=size_value)
                except Size.MultipleObjectsReturned:
                    size = Size.objects.filter(size=size_value).first()
                instance.sizes.add(size)

        return instance

class FileSerialzier(serializers.Serializer):
    file = serializers.FileField()