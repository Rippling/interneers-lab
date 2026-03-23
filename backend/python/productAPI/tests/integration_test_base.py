from django.test import TestCase
from rest_framework.test import APIClient
from productAPI.tests.seed.test_seed import seed_all, clear_all


class IntegrationTestBase(TestCase):
    def setUp(self):
        clear_all()
        self.data = seed_all()
        self.client = APIClient()
        
        self.food_category = self.data["categories"]["food"]
        self.electronics_category = self.data["categories"]["electronics"]
        self.milk = self.data["products"]["milk"]
        self.bread = self.data["products"]["bread"]
        self.phone = self.data["products"]["phone"]

    
    def tearDown(self):
        clear_all()