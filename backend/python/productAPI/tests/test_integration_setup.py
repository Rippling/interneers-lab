from productAPI.models import Product, ProductCategory
from productAPI.tests.integration_test_base import IntegrationTestBase


class TestIntegrationSetup(IntegrationTestBase):

    def test_seed_creates_correct_number_of_products(self):
        count = Product.objects.count()
        self.assertEqual(count, 4)

    def test_seed_creates_correct_number_of_categories(self):
        count = ProductCategory.objects.count()
        self.assertEqual(count, 3)

    def test_seed_products_have_correct_data(self):
        milk = Product.objects(name="Milk").first()
        self.assertIsNotNone(milk)
        self.assertEqual(milk.brand, "Amul")
        self.assertEqual(milk.price, 50)

    def test_seed_category_reference_is_correct(self):
        milk = Product.objects(name="Milk").first()
        self.assertEqual(milk.category.title, "Food")

    def test_isolation_between_tests(self):
        count = Product.objects.count()
        self.assertEqual(count, 4)