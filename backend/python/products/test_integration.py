from django.test import TestCase, Client
from mongoengine import connect, disconnect, get_db
from .models import Product, ProductCategory

class MongoIntegrationTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect(
            db='test_inventory_db', # Note the 'test_' prefix!
            host='localhost',
            port=27019,
            username='root',
            password='example',
            authentication_source='admin'
        )
        super().setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        db = get_db()
        db.client.drop_database('test_inventory_db')
        
        disconnect()
        super().tearDownClass()
        
    def setUp(self):
        self.category = ProductCategory(title="Electronics", description="Gadgets").save()
        
        self.product = Product(
            name="Test Laptop",
            description="A laptop for testing",
            price=999.99,
            quantity=10,
            brand="TestBrand",
            category=self.category
        ).save()
        
        self.client = Client()
        
    def tearDown(self):
        Product.objects.delete()
        ProductCategory.objects.delete()
        
    def test_get_all_products_api(self):
        response = self.client.get('/api/products/')
        
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['name'], "Test Laptop")
        self.assertEqual(data[0]['brand'], "TestBrand")