from rest_framework import serializers
from .models import *


# DEPARTMENT SERIALIZERS
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('department_id', 'name', 'description')
        extra_kwargs = {'description': {'required': True}}


# CATEGORY SERIALIZERS
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'department_id', 'name', 'description')
        # All fields will be required in the request.data
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}


class UpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_id', 'name', 'description')
        # All fields will be required in the request.data
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}


# ATTRIBUTE SERIALIZERS
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('name', )
        extra_kwargs = {'name': {'required': True}}


# ATTRIBUTE VALUE SERIALIZERS
class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('value', )
        extra_kwargs = {'value': {'required': True}}


# PRODUCT SERIALIZERS
class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', )
        # All fields will be required in the request.data
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}


class UpdateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'discounted_price', )
        # All fields will be required in the request.data
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}


class GetProductsSerializer(serializers.Serializer):
    short_product_description_length = serializers.IntegerField()
    products_per_page = serializers.IntegerField()
    start_item = serializers.IntegerField()


class SearchProductsSerializer(serializers.Serializer):
    search_string = serializers.CharField(max_length=256)
    in_all_words = serializers.CharField(max_length=3)
    short_product_description_length = serializers.IntegerField()
    products_per_page = serializers.IntegerField()
    start_item = serializers.IntegerField()


class ProductImageSerializer(serializers.Serializer):
    image = serializers.ImageField(max_length=50)
    option = serializers.ChoiceField(choices=PRODUCT_IMAGES_CHOICES)


class CreateProductReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    review = serializers.CharField(max_length=1024)
    rating = serializers.IntegerField()

    def validate_product_id(self, product_id):
        if not Product.objects.filter(pk=product_id).exists():
            raise serializers.ValidationError('The given Product doesn\'t exists')
        return product_id


class GetProductReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        if not Product.objects.filter(pk=product_id).exists():
            raise serializers.ValidationError('The given Product doesn\'t exists')
        return product_id

