from django.db import IntegrityError
from django.test import TestCase

from products.models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.product_attributes = dict(
            name="Door",
            price=500,
            description="This is a very nice door",
            inventory=5,
        )
        return super().setUp()

    def test_name_not_empty_string(self):
        invalid_attributes = self.product_attributes.copy()
        invalid_attributes["name"] = ""

        with self.assertRaises(IntegrityError):
            Product.objects.create(**invalid_attributes)

    def test_min_price(self):
        invalid_attributes = self.product_attributes.copy()
        invalid_attributes["price"] = 0

        with self.assertRaises(IntegrityError):
            Product.objects.create(**invalid_attributes)

    def test_description_not_empty_string(self):
        invalid_attributes = self.product_attributes.copy()
        invalid_attributes["description"] = ""

        with self.assertRaises(IntegrityError):
            Product.objects.create(**invalid_attributes)

    def test_inventory_not_below_zero(self):
        invalid_attributes = self.product_attributes.copy()
        invalid_attributes["inventory"] = -1

        with self.assertRaises(IntegrityError):
            Product.objects.create(**invalid_attributes)

    def test_inventory_can_be_zero(self):
        invalid_attributes = self.product_attributes.copy()
        invalid_attributes["inventory"] = 0

        Product.objects.create(**invalid_attributes)
        saved_product = Product.objects.first()

        self.assertEqual(saved_product.inventory, 0)
