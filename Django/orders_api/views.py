from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from Django.utils.exec_sp import *
from .serializers import *
import stripe # new
from django.conf import settings
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
def checkout(request):

    if 'total_amount' not in request.query_params:
        msg = {
            "total_amount": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    if 'customer_id' not in request.query_params:
        msg = {
            "customer_id": [
                "You have to login before proceed to checkout.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    if 'cart_id' not in request.query_params:
        msg = {
            "cart_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    if 'shipping_id' not in request.query_params:
        msg = {
            "shipping_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    stripe.Charge.create(
        amount=int(Decimal(request.query_params['total_amount']) * 100),
        currency='usd',
        description='TShirtshop Charge',
        source=request.POST['stripeToken']
    )

    params = [
        request.query_params['cart_id'],
        request.query_params['customer_id'],
        request.query_params['shipping_id'],
        # tax_id
        2,
    ]
    exec_stored_procedure("shopping_cart_create_order", params, False)

    return HttpResponseRedirect(redirect_to=settings.FRONTEND_URL + "/shopping_success")


# Create your views here.
# CUSTOMER VIEWS
@api_view(['GET', 'POST'])
def register_customer(request):
    """
    Register a new Customer account
    """
    if request.method == 'GET':
        return Response(list(ShippingRegion.objects.all().values()))

    else:
        # Validating JSON
        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data
            # Checks if the given shipping_region_id exists or return a 404 Error
            if not ShippingRegion.objects.filter(pk=valid_data['shipping_region_id']).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)

            Customer.objects.create_user(email=valid_data['email'], password=valid_data['password'],
                                         name=valid_data['name'], shipping_region_id=valid_data['shipping_region_id'])

            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def customer(request):
    """
       Retrieves or Updates a Customer.
    """
    # Checks if the instance exists or return a 404 Error
    params = [request.user.customer_id, ]
    cus = exec_stored_procedure("customer_get_customer", params, True)
    if cus.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # If the instance exists then retrieve the data.
    if request.method == 'GET':
        return Response(cus[0])

    elif request.method == 'PUT':
        # Validating JSON
        serializer = UpdateCustomerAccountSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the customer account
            c = Customer.objects.get(pk=request.user.customer_id)
            c.name = valid_data['name']
            c.day_phone = valid_data['day_phone']
            c.eve_phone = valid_data['eve_phone']
            c.mob_phone = valid_data['mob_phone']
            c.save()

            # Getting the updated product
            params = [request.user.customer_id, ]
            cus = exec_stored_procedure("customer_get_customer", params, True)
            return Response(cus[0])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def customer_update_address(request):
    """
       Retrieves or Updates a Customer.
    """
    # Checks if the instance exists or return a 404 Error
    params = [request.user.customer_id, ]
    cus = exec_stored_procedure("customer_get_customer", params, True)
    if cus.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        # Validating JSON
        serializer = UpdateCustomerAddressSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the customer account
            params = [
                request.user.customer_id,
                valid_data['address_1'],
                valid_data['address_2'],
                valid_data['city'],
                valid_data['region'],
                valid_data['postal_code'],
                valid_data['country'],
                valid_data['shipping_region_id'],
            ]
            exec_stored_procedure("customer_update_address", params, False)

            # Getting the updated product
            params = [request.user.customer_id, ]
            cus = exec_stored_procedure("customer_get_customer", params, True)
            return Response(cus[0])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def customer_update_credit_card(request):
    """
       Retrieves or Updates a Customer.
    """
    # Checks if the instance exists or return a 404 Error
    params = [request.user.customer_id, ]
    cus = exec_stored_procedure("customer_get_customer", params, True)
    if cus.__len__() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        # Validating JSON
        serializer = UpdateCustomerCreditCardSerializer(data=request.data)
        if serializer.is_valid():
            valid_data = serializer.validated_data

            # Updating the customer account
            params = [
                request.user.customer_id,
                valid_data['credit_card'],
            ]
            exec_stored_procedure("customer_update_credit_card", params, False)

            # Getting the updated product
            params = [request.user.customer_id, ]
            cus = exec_stored_procedure("customer_get_customer", params, True)
            return Response(cus[0])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# SHOPPING_CART VIEWS
@api_view(['POST'])
def shopping_cart_add_product(request):
    """
    Adds a product to a given shopping cart, if the shopping cart not exists or is null then creates a new shopping cart
    """
    # Validating JSON
    serializer = ShoppingCartAddProductSerializer(data=request.data)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['cart_id'],
            valid_data['product_id'],
            valid_data['attributes'],
        ]
        if valid_data['cart_id'] == "":
            return Response(exec_stored_procedure("shopping_cart_add_product", params, True))
        else:
            exec_stored_procedure("shopping_cart_add_product", params, False)
            return Response()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def shopping_cart_update(request):
    """
    Adds a product to a given shopping cart, if the shopping cart not exists or is null then creates a new shopping cart
    """
    # Validating JSON
    serializer = ShoppingCartUpdateSerializer(data=request.data)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['item_id'],
            valid_data['quantity'],
        ]
        exec_stored_procedure("shopping_cart_update", params, False)
        return Response()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def shopping_cart_create_order(request):
    """
    Creates a new Order
    """
    # Validating JSON
    serializer = ShoppingCartCreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['cart_id'],
            request.user.customer_id,
            valid_data['shipping_id'],
            valid_data['tax_id'],
        ]
        exec_stored_procedure("shopping_cart_create_order", params, False)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def shopping_cart_get_products(request):
    """
       Retrieves the products for a given cart_id.
    """

    # Validating JSON
    serializer = ShoppingCartId(data=request.query_params)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['cart_id'],
        ]
        total_amount = exec_stored_procedure("shopping_cart_get_total_amount", params, True)[0]['total_amount']

        resp = {
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'total_amount': total_amount,
            'customer_id': request.user.customer_id,
            'products': exec_stored_procedure("shopping_cart_get_products", params, True),
        }

        return Response(resp)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def shopping_cart_get_saved_products(request):
    """
       Retrieves the saved products for a given cart_id.
    """

    # Validating JSON
    serializer = ShoppingCartId(data=request.query_params)
    if serializer.is_valid():
        valid_data = serializer.validated_data
        params = [
            valid_data['cart_id'],
        ]

        return Response(exec_stored_procedure("shopping_cart_get_saved_products", params, True))
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def shopping_cart_remove_products(request):
    """
       Removes a product from a given shopping cart
    """

    # Validating JSON
    if 'item_id' in request.data:
        item_id = request.data['item_id']
        if ShoppingCart.objects.filter(item_id=item_id).exists():
            params = [
                item_id,
            ]

            exec_stored_procedure("shopping_cart_remove_product", params, False)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        msg = {
            "item_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def shopping_cart_save_product_for_later(request):
    """
       Saves a product for later
    """

    # Validating JSON
    if 'item_id' in request.data:
        item_id = request.data['item_id']
        if ShoppingCart.objects.filter(item_id=item_id).exists():
            params = [
                item_id,
            ]

            exec_stored_procedure("shopping_cart_save_product_for_later", params, False)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        msg = {
            "item_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def shopping_cart_move_product_to_cart(request):
    """
       Moves a product to the shopping cart
    """

    # Validating JSON
    if 'item_id' in request.data:
        item_id = request.data['item_id']
        if ShoppingCart.objects.filter(item_id=item_id).exists():
            params = [
                item_id,
            ]

            exec_stored_procedure("shopping_cart_move_product_to_cart", params, False)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        msg = {
            "item_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


# ORDER VIEWS
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def orders_get_by_customer_id(request):
    """
       Retrieves orders placed by a customer
    """
    # Validating JSON
    params = [
        request.user.customer_id,
    ]

    return Response(exec_stored_procedure("orders_get_by_customer_id", params, True))


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_order_details(request):
    """
       Get the details for a order
    """
    if 'order_id' in request.query_params:
        order_id = request.query_params['order_id']
        if Orders.objects.filter(pk=order_id).exists():
            params = [
                order_id,
            ]

            return Response(exec_stored_procedure("orders_get_order_details", params, True))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        msg = {
            "order_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_order_info(request):
    """
       Get the order info
    """
    if 'order_id' in request.query_params:
        order_id = request.query_params['order_id']
        if Orders.objects.filter(pk=order_id).exists():
            params = [
                order_id,
            ]

            return Response(exec_stored_procedure("orders_get_order_info", params, True))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        msg = {
            "order_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_order_short_details(request):
    """
       Get the short details for a order
    """
    if 'order_id' in request.query_params:
        order_id = request.query_params['order_id']
        if Orders.objects.filter(pk=order_id).exists():
            params = [
                order_id,
            ]

            return Response(exec_stored_procedure("orders_get_order_short_details", params, True))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    else:
        msg = {
            "order_id": [
                "This field is required.",
            ]
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_shipping_options(request):
    """
    Retrieves the shipping options for a customer by their shipping region
    """
    return Response(list(Shipping.objects.filter(shipping_region_id=request.user.shipping_region_id).values()))