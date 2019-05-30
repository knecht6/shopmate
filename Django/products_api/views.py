import re, os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import FileSystemStorage
from Django.utils.exec_sp import *
from .models import PRODUCT_IMAGES_DIRECTORY
from .serializers import *


def get_image_name(product_name, image_name, option):
    image_extension = os.path.splitext(image_name)[1]

    # Removing special characters
    s = re.sub('[^A-Za-z0-9 ]+', '', product_name)
    # Removing multiple white spaces
    s = re.sub(' +', ' ', s)
    # Converting white spaces to hyphen character '-'
    s = re.sub(' ', '-', s).lower()

    if option == '2':
        # If this image is to set image-2, then add '-2' to the filename
        s = s + '-2'
    elif option == '3':
        # If this image is to set thumbnail, then add '-thumbnail' to the filename
        s = s + '-thumbnail'

    return s + image_extension


# Create your views here.
# PRODUCTS VIEWS
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_product_review(request):
    """
    Creates a product review.
    """

    # Validating JSON
    serializer = CreateProductReviewSerializer(data=request.data)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            request.user.customer_id,
            valid_data['product_id'],
            valid_data['review'],
            valid_data['rating'],
        ]
        exec_stored_procedure("catalog_create_product_review", params, False)
        return Response()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_product_reviews(request):
    """
    Gets all reviews for a given product.
    """

    # Validating JSON
    serializer = GetProductReviewSerializer(data=request.query_params)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['product_id'],
        ]
        return Response(exec_stored_procedure("catalog_get_product_reviews", params, True))
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def products_on_department(request, department_id):
    """
    Retrieves the products for a given department_id
    """
    # Checks if the given department_id exists or return a 404 Error
    params = [department_id, ]
    cat = exec_stored_procedure("catalog_get_department_details", params, True)
    if cat.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Validating JSON
    serializer = GetProductsSerializer(data=request.query_params)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            department_id,
            valid_data['short_product_description_length'],
            valid_data['products_per_page'],
            valid_data['start_item'],
        ]

        return Response(exec_stored_procedure("catalog_get_products_on_department", params, True))
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def products_in_category(request, category_id):
    """
    Retrieves all Products in a Category or Creates a new Product in a Category.
    """
    # Checks if the given category_id exists or return a 404 Error
    params = [category_id, ]
    cat = exec_stored_procedure("catalog_get_category_details", params, True)
    if cat.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Validating JSON
        serializer = GetProductsSerializer(data=request.query_params)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            params = [
                category_id,
                valid_data['short_product_description_length'],
                valid_data['products_per_page'],
                valid_data['start_item'],
            ]

            return Response(exec_stored_procedure("catalog_get_products_in_category", params, True))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Validating JSON
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            params = [
                category_id,
                valid_data['name'],
                valid_data['description'],
                valid_data['price'],
            ]
            exec_stored_procedure("catalog_add_product_to_category", params, False)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product(request, pk):
    """
    Retrieves, Updates or Deletes a Product.
    """
    # Checks if the instance exists or return a 404 Error
    params = [str(pk), ]
    prod = exec_stored_procedure("catalog_get_product_details", params, True)
    if prod.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the instance exists then retrieve the data.
    if request.method == 'GET':
        return Response(prod[0])

    elif request.method == 'PUT':
        # Validating JSON
        serializer = UpdateProductSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the department
            params = [
                str(pk),
                valid_data['name'],
                valid_data['description'],
                valid_data['price'],
                valid_data['discounted_price'],
            ]
            exec_stored_procedure("catalog_update_product", params, False)

            # Getting the updated product
            params = [str(pk), ]
            prod = exec_stored_procedure("catalog_get_product_details", params, True)
            return Response(prod[0])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exec_stored_procedure("catalog_delete_product", params, False)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def products_on_catalog(request):
    """
    Retrieves all Products on Catalog.
    """

    # Validating JSON
    serializer = GetProductsSerializer(data=request.query_params)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['short_product_description_length'],
            valid_data['products_per_page'],
            valid_data['start_item'],
        ]
        return Response(exec_stored_procedure("catalog_get_products_on_catalog", params, True))
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def set_image(request, pk):
    """
    Sets the image or image1 or thumbnail to a given product.
    """
    # Checks if the instance exists or return a 404 Error
    params = [str(pk), ]
    prod = exec_stored_procedure("catalog_get_product_info", params, True)
    if prod.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the instance exists then update the image.
    # Validating JSON
    serializer = ProductImageSerializer(data=request.data)
    if serializer.is_valid():
        fs = FileSystemStorage()
        valid_data = serializer.validated_data
        image_type = get_image_display(valid_data['option'])
        # Deleting the actual image
        if prod[0][image_type] != "":
            image_path = PRODUCT_IMAGES_DIRECTORY + "/" + prod[0][image_type]
            if fs.exists(image_path):
                fs.delete(image_path)

        # Adding the new image
        image = valid_data['image']
        image_name = get_image_name(prod[0]['name'], image.name, valid_data['option'])
        image_path = PRODUCT_IMAGES_DIRECTORY + "/" + image_name
        fs.save(image_path, image)

        # Updating the image_1 of the product.
        params = [
            str(pk),
            image_name,
        ]
        exec_stored_procedure("catalog_set_" + image_type, params, False)

        return Response()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def catalog_search(request):
    """
    Searches products on the Catalog and Retrieves the output.
    """

    # Validating JSON
    serializer = SearchProductsSerializer(data=request.query_params)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['search_string'],
            valid_data['in_all_words'],
            valid_data['short_product_description_length'],
            valid_data['products_per_page'],
            valid_data['start_item'],
        ]
        return Response(exec_stored_procedure("catalog_search", params, True))
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DEPARTMENT VIEWS
@api_view(['GET', 'POST'])
def departments(request):
    """
    Retrieves all Departments or Creates a new Department.
    """
    if request.method == 'GET':
        return Response(exec_stored_procedure("catalog_get_departments", None, True))
    else:
        # Validating JSON
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            params = [
                valid_data['name'],
                valid_data['description']
            ]
            exec_stored_procedure("catalog_add_department", params, False)
            return Response(exec_stored_procedure("catalog_get_departments", None, True), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def department(request, pk):
    """
    Retrieves, Updates or Deletes a Department.
    """
    # Checks if the instance exists or return a 404 Error
    params = [str(pk), ]
    dept = exec_stored_procedure("catalog_get_department_details", params, True)
    if dept.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the instance exists then retrieve the data.
    if request.method == 'GET':
        return Response(dept[0])

    elif request.method == 'PUT':
        # Validating JSON
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the department
            params = [
                str(pk),
                valid_data['name'],
                valid_data['description'],
            ]
            exec_stored_procedure("catalog_update_department", params, False)

            # Getting the updated department
            params = [str(pk), ]
            dept = exec_stored_procedure("catalog_get_department_details", params, True)
            return Response(dept[0])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        deleted = exec_stored_procedure("catalog_delete_department", params, True)
        if deleted[0].__contains__('1'):
            # Deleted successfully
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Error while deleting
            err = {"Check Foreign": ["Cannot delete this instance"]}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# CATEGORY VIEWS
@api_view(['GET', 'POST'])
def categories(request):
    """
    Retrieves all Categories or Creates a new Category.
    """
    if request.method == 'GET':
        return Response(exec_stored_procedure("catalog_get_categories", None, True))
    else:
        # Validating JSON
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            params = [valid_data['department_id'], ]
            # Validating that the given department_id already exists.
            dept = exec_stored_procedure("catalog_get_department_details", params, True)
            if dept.__len__() == 0:
                msg = {
                    "department_id": [
                        "The given department_id doesn't exists"
                    ]
                }
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)

            # If the department_id exists, then add the new Category.
            params = [
                valid_data['department_id'],
                valid_data['name'],
                valid_data['description']
            ]
            exec_stored_procedure("catalog_add_category", params, False)
            return Response(exec_stored_procedure("catalog_get_categories", None, True), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category(request, pk):
    """
    Retrieves, Updates or Deletes a Category.
    """
    # Checks if the instance exists or return a 404 Error
    params = [str(pk), ]
    cat = exec_stored_procedure("catalog_get_category_details", params, True)
    if cat.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the instance exists then retrieve the data.
    if request.method == 'GET':
        return Response(cat[0])

    elif request.method == 'PUT':
        # Validating JSON
        serializer = UpdateCategorySerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the Category
            params = [
                str(pk),
                valid_data['name'],
                valid_data['description'],
            ]
            exec_stored_procedure("catalog_update_category", params, False)

            # Getting the updated category
            params = [str(pk), ]
            cat = exec_stored_procedure("catalog_get_category_details", params, True)
            return Response(cat[0])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        deleted = exec_stored_procedure("catalog_delete_category", params, True)
        if deleted[0].__contains__('1'):
            # Deleted successfully
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Error while deleting
            err = {"Check Foreign": ["Cannot delete this instance"]}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def categories_list(request, department_id):
    """
    Retrieves a list of categories for a given department_id
    """

    # Validating that the given department_id already exists.
    params = [
        department_id,
    ]
    dept = exec_stored_procedure("catalog_get_department_details", params, True)
    if dept.__len__() == 0:
        msg = {
            "department_id": [
                "The given department_id doesn't exists"
            ]
        }
        return Response(msg, status=status.HTTP_404_NOT_FOUND)

    # If the department_id exists then retrieve the list of categories.
    return Response(exec_stored_procedure("catalog_get_categories_list", params, True))


# ATTRIBUTE VIEWS
@api_view(['GET', 'POST'])
def attributes(request):
    """
    Retrieves all Attributes or Creates a new Attribute.
    """
    if request.method == 'GET':
        return Response(exec_stored_procedure("catalog_get_attributes", None, True))
    else:
        # Validating JSON
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            params = [valid_data['name'], ]
            exec_stored_procedure("catalog_add_attribute", params, False)
            return Response(exec_stored_procedure("catalog_get_attributes", None, True), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def attribute(request, pk):
    """
    Retrieves, Updates or Deletes an Attribute.
    """
    # Checks if the instance exists or return a 404 Error
    params = [str(pk), ]
    attr = exec_stored_procedure("catalog_get_attribute_details", params, True)
    if attr.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the instance exists then retrieve the data.
    if request.method == 'GET':
        return Response(attr[0])

    elif request.method == 'PUT':
        # Validating JSON
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the attribute
            params = [
                str(pk),
                valid_data['name'],
            ]
            exec_stored_procedure("catalog_update_attribute", params, False)

            # Getting the updated attribute
            params = [str(pk), ]
            attr = exec_stored_procedure("catalog_get_attribute_details", params, True)
            return Response(attr[0])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        deleted = exec_stored_procedure("catalog_delete_attribute", params, True)
        if deleted[0].__contains__('1'):
            # Deleted successfully
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Error while deleting
            err = {"Check Foreign": ["Cannot delete this instance"]}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)


# ATTRIBUTE VALUE VIEWS
@api_view(['GET', 'POST'])
def attribute_values(request, attribute_id):
    """
    Retrieves all Attribute values of an Attribute instance or Creates a new Attribute Value for a given
    Attribute instance.
    """
    # Checks if the given attribute_id exists or return a 404 Error
    params = [attribute_id, ]
    attr = exec_stored_procedure("catalog_get_attribute_details", params, True)
    if attr.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(exec_stored_procedure("catalog_get_attribute_values", params, True))
    else:
        # Validating JSON
        serializer = AttributeValueSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            params = [
                attribute_id,
                valid_data['value']
            ]
            exec_stored_procedure("catalog_add_attribute_value", params, False)

            params = [attribute_id, ]
            return Response(exec_stored_procedure("catalog_get_attribute_values", params, True),
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def attribute_value(request, pk):
    """
    Updates or Deletes an AttributeValue.
    """
    # Checks if the instance exists or return a 404 Error
    try:
        AttributeValue.objects.get(pk=pk)
    except AttributeValue.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Validating JSON
        serializer = AttributeValueSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the AttributeValue
            params = [
                pk,
                valid_data['value'],
            ]
            exec_stored_procedure("catalog_update_attribute_value", params, False)
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        params = [pk, ]
        deleted = exec_stored_procedure("catalog_delete_attribute_value", params, True)
        if deleted[0].__contains__('1'):
            # Deleted successfully
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Error while deleting
            err = {"Check Foreign": ["Cannot delete this instance"]}
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
