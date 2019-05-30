from rest_framework import serializers
from .models import *


# CUSTOMER SERIALIZERS
class RegisterCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('name', 'email', 'password', 'shipping_region_id', )


class UpdateCustomerAccountSerializer(serializers.ModelSerializer):

    def validate_shipping_region_id(self, shipping_regions_id):
        if not ShippingRegion.objects.filter(pk=shipping_regions_id).exists():
            raise serializers.ValidationError('The given Shipping Region doesn\'t exists')
        return shipping_regions_id

    class Meta:
        model = Customer
        fields = ('name', 'day_phone', 'eve_phone', 'mob_phone', )
        # All fields will be required in the request.data
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}


class UpdateCustomerAddressSerializer(serializers.ModelSerializer):

    def validate_shipping_region_id(self, shipping_regions_id):
        if not ShippingRegion.objects.filter(pk=shipping_regions_id).exists():
            raise serializers.ValidationError('The given Shipping Region doesn\'t exists')
        return shipping_regions_id

    class Meta:
        model = Customer
        fields = ('address_1', 'address_2', 'city', 'region', 'postal_code', 'country', 'shipping_region_id', )
        # All fields will be required in the request.data
        extra_kwargs = {}
        for field in fields:
            extra_kwargs[field] = {'required': True}


class UpdateCustomerCreditCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('credit_card', )
        extra_kwargs = {'credit_card': {'required': True}}


# SHOPPING_CART SERIALIZERS
class ShoppingCartAddProductSerializer(serializers.ModelSerializer):

    def validate_cart_id(self, cart_id):
        if cart_id != "" and not ShoppingCart.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('The given Shopping Cart doesn\'t exists')
        return cart_id

    class Meta:
        model = ShoppingCart
        fields = ('cart_id', 'product_id', 'attributes', )
        extra_kwargs = {}
        extra_kwargs['product_id'] = {'required': True}
        extra_kwargs['attributes'] = {'required': True}
        extra_kwargs['cart_id'] = {'required': True, 'allow_blank': True}


class ShoppingCartCreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.CharField(max_length=32)
    shipping_id = serializers.IntegerField()
    tax_id = serializers.IntegerField()

    def validate_cart_id(self, cart_id):
        if not ShoppingCart.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('The given Shopping Cart doesn\'t exists')
        return cart_id

    def validate_shipping_id(self, shipping_id):
        if not Shipping.objects.filter(pk=shipping_id).exists():
            raise serializers.ValidationError('The given Shipping doesn\'t exists')
        return shipping_id

    def validate_tax_id(self, tax_id):
        if not Tax.objects.filter(pk=tax_id).exists():
            raise serializers.ValidationError('The given Tax doesn\'t exists')
        return tax_id


class ShoppingCartId(serializers.ModelSerializer):

    def validate_cart_id(self, cart_id):
        if not ShoppingCart.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('The given Shopping Cart doesn\'t exists')
        return cart_id

    class Meta:
        model = ShoppingCart
        fields = ('cart_id', )
        extra_kwargs = {'cart_id': {'required': True}}


class ShoppingCartUpdateSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_item_id(self, item_id):
        if not ShoppingCart.objects.filter(item_id=item_id).exists():
            raise serializers.ValidationError('The given item_id doesn\'t exists')
        return item_id
