import os
from django.db.utils import OperationalError
from Django.tshirtshop.settings import BASE_DIR
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Orders, Customer, ShoppingCart


def setup_test_environment():
    from django.db import connection
    try:
        connection.cursor().execute("DROP DATABASE test_tshirtshop")
    except OperationalError:
        print("Can't drop database 'test_tshirtshop'; database doesn't exist")

    connection.cursor().execute("CREATE DATABASE test_tshirtshop CHARACTER SET UTF8")
    connection.cursor().execute("USE test_tshirtshop;")
    # Get current directory
    file_path = os.path.join(BASE_DIR, 'utils/create_test_tables.txt')
    file = open(file_path)
    delimiter = ";\n"
    statement = ""

    for row in file.readlines():
        # Ignore comments or line break
        if not (row.startswith("--") or row == "" or row == "\n"):
            if row.upper().__contains__("DELIMITER"):
                # Set a new delimiter
                delimiter = row.upper().split(" ")[-1]
            else:
                if row.__contains__("--"):
                    row = row.split("-- ")[0]

                statement += row
                if row.__contains__(delimiter):
                    statement = statement.replace(delimiter, "").replace("\n", "")
                    # print(statement)
                    connection.cursor().execute(statement)
                    statement = ""

    file.close()


# Create your tests here.
class OrderTests(APITestCase):

    def setUp(self):
        setup_test_environment()

    def test_create_order(self):
        """
        Ensure we can create a new order object.
        """
        client = APIClient()
        # First create a user
        Customer.objects.create_user(name="kevin", email="re14001@turing.com", password="secret_pass",
                                     shipping_region_id=1)

        # Then force login with that user
        url = reverse('login')
        data = {'email': "re14001@turing.com", 'password': "secret_pass"}
        response = client.post(url, data, format='json')
        access_token = response.data['access']

        # Then add products to the shopping cart
        url = reverse('shopping_cart_add_product')
        data = {'cart_id': "", 'product_id': 1, 'attributes': "Blue, XL"}
        response = client.post(url, data, format='json')
        cart_id = response.data[0]['cart_id']

        url = reverse('shopping_cart_create_order')
        data = {'cart_id': cart_id, 'shipping_id': 1, 'tax_id': 1}
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Orders.objects.count(), 1)


class CreateShoppingCartTests(APITestCase):

    def setUp(self):
        setup_test_environment()

    def test_create_shopping_cart(self):
        """
        Ensure we can create a new order object.
        """
        client = APIClient()
        # First create a user
        Customer.objects.create_user(name="kevin", email="re14001@turing.com", password="secret_pass",
                                     shipping_region_id=1)

        # Then force login with that user
        url = reverse('login')
        data = {'email': "re14001@turing.com", 'password': "secret_pass"}
        response = client.post(url, data, format='json')
        access_token = response.data['access']

        # Then add products to the shopping cart
        url = reverse('shopping_cart_add_product')
        data = {'cart_id': "", 'product_id': 1, 'attributes': "Blue, XL"}
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['item_id'], 1)
        self.assertEqual(ShoppingCart.objects.count(), 1)


class DeleteShoppingCartItemTests(APITestCase):

    def setUp(self):
        setup_test_environment()

    def test_delete_shopping_cart_item(self):
        """
        Ensure we can delete an item from shopping cart.
        """
        client = APIClient()
        # First create a user
        Customer.objects.create_user(name="kevin", email="re14001@turing.com", password="secret_pass",
                                     shipping_region_id=1)

        # Then force login with that user
        url = reverse('login')
        data = {'email': "re14001@turing.com", 'password': "secret_pass"}
        response = client.post(url, data, format='json')
        access_token = response.data['access']

        # Then add products to the shopping cart
        url = reverse('shopping_cart_add_product')
        data = {'cart_id': "", 'product_id': 1, 'attributes': "Blue, XL"}
        response = client.post(url, data, format='json')
        item_id = response.data[0]['item_id']

        url = reverse('shopping_cart_remove_products')
        data = {'item_id': item_id, }
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShoppingCart.objects.count(), 0)


class UpdateShoppingCartTests(APITestCase):

    def setUp(self):
        setup_test_environment()

    def test_create_shopping_cart(self):
        """
        Ensure we can create a new order object.
        """
        client = APIClient()
        # First create a user
        Customer.objects.create_user(name="kevin", email="re14001@turing.com", password="secret_pass",
                                     shipping_region_id=1)

        # Then force login with that user
        url = reverse('login')
        data = {'email': "re14001@turing.com", 'password': "secret_pass"}
        response = client.post(url, data, format='json')
        access_token = response.data['access']

        # Then add products to the shopping cart
        url = reverse('shopping_cart_add_product')
        data = {'cart_id': "", 'product_id': 1, 'attributes': "Blue, XL"}
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = client.post(url, data, format='json')
        item_id = response.data[0]['item_id']

        # Then update the shopping cart
        url = reverse('shopping_cart_update')
        data = {'item_id': item_id, 'quantity': 5}
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ShoppingCart.objects.get(pk=item_id).quantity, 5)
        self.assertEqual(ShoppingCart.objects.count(), 1)
