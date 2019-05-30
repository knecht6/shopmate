from django.db import models

PRODUCT_IMAGES_DIRECTORY = "product_images"
PRODUCT_IMAGES_CHOICES = (('1', 'image'), ('2', 'image_2'), ('3', 'thumbnail'))


def get_image_display(option):
    for opt in PRODUCT_IMAGES_CHOICES:
        if option == opt[0]:
            return opt[1]


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'department'
        managed = False


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    department_id = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'category'
        managed = False


class Attribute(models.Model):
    attribute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'attribute'
        managed = False


class AttributeValue(models.Model):
    attribute_value_id = models.AutoField(primary_key=True)
    attribute_id = models.IntegerField()
    value = models.CharField(max_length=100)

    class Meta:
        db_table = 'attribute_value'
        managed = False


class ProductAttribute(models.Model):
    product_id = models.IntegerField(primary_key=True)
    attribute_value_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_attribute'
        unique_together = (('product_id', 'attribute_value_id'),)


class ProductCategory(models.Model):
    product_id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_category'
        unique_together = (('product_id', 'category_id'),)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=150, blank=True, null=True)
    image_2 = models.CharField(max_length=150, blank=True, null=True)
    thumbnail = models.CharField(max_length=150, blank=True, null=True)
    display = models.SmallIntegerField()

    class Meta:
        db_table = 'product'
        managed = False
