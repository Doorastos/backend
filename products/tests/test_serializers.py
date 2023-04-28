from django.test import TestCase

from ..models import Product
from ..serializers import ProductSerializer


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.valid_serializer_input = dict(
            name="Door",
            price=500.00,
            description="This is a very nice door",
            inventory=5,
        )
        self.product = Product.objects.create(**self.valid_serializer_input)
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

    def test_valid_input_data(self):
        valid_serializer_input = self.valid_serializer_input.copy()
        valid_serializer_input["name"] = "Different door"  # Name has unique constraint
        serialized_data = ProductSerializer(data=valid_serializer_input)

        self.assertTrue(serialized_data.is_valid())

    def test_name_not_empty_string(self):
        invalid_serializer_input = self.valid_serializer_input.copy()
        invalid_serializer_input["name"] = ""
        serialized_data = ProductSerializer(data=invalid_serializer_input)

        self.assertFalse(serialized_data.is_valid())

    def test_min_price(self):
        invalid_serializer_input = self.valid_serializer_input.copy()
        invalid_serializer_input["name"] = "Min price"  # Name has unique constraint
        invalid_serializer_input["price"] = 0
        serialized_data = ProductSerializer(data=invalid_serializer_input)

        self.assertFalse(serialized_data.is_valid())

    def test_description_not_empty_string(self):
        invalid_serializer_input = self.valid_serializer_input.copy()
        invalid_serializer_input["name"] = "Desc != ''"  # Name has unique constraint
        invalid_serializer_input["description"] = ""
        serialized_data = ProductSerializer(data=invalid_serializer_input)

        self.assertFalse(serialized_data.is_valid())

    def test_inventory_not_below_zero(self):
        invalid_serializer_input = self.valid_serializer_input.copy()
        invalid_serializer_input["name"] = "Inv > 0"  # Name has unique constraint
        invalid_serializer_input["inventory"] = -1
        serialized_data = ProductSerializer(data=invalid_serializer_input)

        self.assertFalse(serialized_data.is_valid())

    def test_inventory_can_be_zero(self):
        valid_serializer_input = self.valid_serializer_input.copy()
        valid_serializer_input["name"] = "Inv == 0"  # Name has unique constraint
        valid_serializer_input["inventory"] = 0
        serialized_data = ProductSerializer(data=valid_serializer_input)

        self.assertTrue(serialized_data.is_valid())
