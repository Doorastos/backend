from django.db import IntegrityError, models


class Product(models.Model):
    """DB model representing a single product."""

    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    inventory = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        """Validate and save the instance."""
        min_len_name = 1
        min_price = 0.5
        min_len_description = 1

        if (
            len(self.name) < min_len_name
            or self.price < min_price
            or len(self.description) < min_len_description
        ):
            raise IntegrityError()
        return super().save(*args, **kwargs)
