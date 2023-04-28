from django.test import TestCase

from ..models import Product
from ..serializers import ProductSerializer


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Door",
            price=500.00,
            description="This is a very nice door",
            inventory=5,
        )
        self.serialized_product = ProductSerializer(instance=self.product)

        self.expected_model_fields = [
            "id",
            "name",
            "price",
            "description",
            "inventory",
        ]
        self.expected_model_field_values = {
            "id": self.product.id,
            "name": self.product.name,
            "price": f"{self.product.price:.2f}",  # Decimal fields return strings
            "description": self.product.description,
            "inventory": self.product.inventory,
        }
        return super().setUp()

    def test_contains_expected_fields(self):
        data = self.serialized_product.data
        self.assertEqual(data.keys(), set(self.expected_model_fields))

    def test_contains_expected_values(self):
        data = self.serialized_product.data
        self.assertEqual(data, self.expected_model_field_values)
