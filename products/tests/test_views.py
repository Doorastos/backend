from django.test import TestCase
from rest_framework import status

from ..models import Product
from ..views import ProductListView

EXPECTED_CONTENT_TYPE = "application/json"


class ProductViewTest(TestCase):
    def setUp(self):
        self.url = "/api/products"
        self.view = ProductListView

        self.product_data = dict(
            name="Door",
            price=500,
            description="This is a very nice door",
            inventory=5,
        )

        return super().setUp()

    def test_default_content_type(self):
        response = self.client.get(self.url)

        self.assertEqual(response["Content-Type"], EXPECTED_CONTENT_TYPE)

    def test_url_resolve_to_correct_view(self):
        response = self.client.get(self.url)

        self.assertIs(response.resolver_match.func.view_class, self.view)

    def test_save_product_on_POST(self):
        response = self.client.post(self.url, data=self.product_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, self.product_data["name"])

    def test_list_all_books_on_GET(self):
        door1 = self.product_data.copy()
        door1["name"] = "door1 on GET"
        self.client.post(self.url, data=door1)
        door2 = self.product_data.copy()
        door2["name"] = "door2 on GET"
        self.client.post(self.url, data=door2)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": 1,
                    "name": "door1 on GET",
                    "price": "500.00",
                    "description": "This is a very nice door",
                    "inventory": 5,
                },
                {
                    "id": 2,
                    "name": "door2 on GET",
                    "price": "500.00",
                    "description": "This is a very nice door",
                    "inventory": 5,
                },
            ],
        )
