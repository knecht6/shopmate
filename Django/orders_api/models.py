from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.


class Audit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    created_on = models.DateTimeField()
    message = models.TextField()
    code = models.IntegerField()

    class Meta:
        db_table = 'audit'
        managed = False


class CustomerUserManager(BaseUserManager):

    def create_user(self, name, email, password, **extra_fields):
        email = self.normalize_email(email)
        customer = self.model(name=name, email=email, shipping_region_id=extra_fields['shipping_region_id'])
        customer.set_password(password)
        customer.save(using=self._db)
        return customer

    def create_superuser(self, name, email, password, **extra_fields):
        email = self.normalize_email(email)
        customer = self.model(name=name, email=email, shipping_region_id=extra_fields['shipping_region_id'])
        customer.set_password(password)
        customer.save(using=self._db)
        return customer


class Customer(AbstractBaseUser):
    REQUIRED_FIELDS = ('name', 'password', 'shipping_region_id')
    USERNAME_FIELD = 'email'

    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=50)
    credit_card = models.TextField(blank=True, null=True)
    address_1 = models.CharField(max_length=100, blank=True, null=True)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    shipping_region_id = models.IntegerField()
    day_phone = models.CharField(max_length=100, blank=True, null=True)
    eve_phone = models.CharField(max_length=100, blank=True, null=True)
    mob_phone = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomerUserManager()

    class Meta:
        db_table = 'customer'
        managed = False


class OrderDetail(models.Model):
    item_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    attributes = models.CharField(max_length=1000)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_detail'
        managed = False


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField()
    shipped_on = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    comments = models.CharField(max_length=255, blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    auth_code = models.CharField(max_length=50, blank=True, null=True)
    reference = models.CharField(max_length=50, blank=True, null=True)
    shipping_id = models.IntegerField(blank=True, null=True)
    tax_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'orders'
        managed = False


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    review = models.TextField()
    rating = models.SmallIntegerField()
    created_on = models.DateTimeField()

    class Meta:
        db_table = 'review'
        managed = False


class Shipping(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    shipping_type = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_region_id = models.IntegerField()

    class Meta:
        db_table = 'shipping'
        managed = False


class ShippingRegion(models.Model):
    shipping_region_id = models.AutoField(primary_key=True)
    shipping_region = models.CharField(max_length=100)

    class Meta:
        db_table = 'shipping_region'
        managed = False


class ShoppingCart(models.Model):
    item_id = models.AutoField(primary_key=True)
    cart_id = models.CharField(max_length=32)
    product_id = models.IntegerField()
    attributes = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    buy_now = models.IntegerField()
    added_on = models.DateTimeField()

    class Meta:
        db_table = 'shopping_cart'
        managed = False


class Tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_type = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'tax'
        managed = False

