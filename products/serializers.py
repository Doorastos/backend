from rest_framework.serializers import ModelSerializer

from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "inventory",
        ]
        extra_kwargs = {
            # Extra validation layer to reduce DB load and risk of integrity error.
            # WARNING: Ensure these match min values set in model definition.
            "name": {"min_length": 1},
            "price": {"min_value": 0.5},
            "description": {"min_length": 1},
            "inventory": {"min_value": 0},
        }
