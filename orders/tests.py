from django.test import TestCase
from . import helpers


# Create Product
class CreateProductTest(TestCase):

    def test_create_product(self):
        product_data = {
            'name': 'guazamamaya',
            'price': 50.00,
            'stock': 2
        }
        # Create
        response = helpers.save_product_info(product_data)
        new = {
            'id': response.id,
            'stock': 50
        }
        # Update
        res = helpers.update_product_stock(new)

        return f'{response}'
