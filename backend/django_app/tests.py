from django.test import TestCase, Client
from django.urls import reverse
import json
from urllib.parse import quote

class HelloNameEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('hello_name')  # This will resolve to '/hello/'

    def test_hello_without_name(self):
        """Test the endpoint when no name parameter is provided"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Hello, World!')

    def test_hello_with_name(self):
        """Test the endpoint when a name parameter is provided"""
        test_name = 'Alice'
        response = self.client.get(f'{self.url}?name={test_name}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertEqual(data['message'], f'Hello, {test_name}!')

    def test_hello_with_empty_name(self):
        """Test the endpoint when an empty name parameter is provided"""
        response = self.client.get(f'{self.url}?name=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Hello, !')

    def test_hello_with_special_characters(self):
        """Test the endpoint with special characters in the name"""
        test_name = 'John Doe!@#'
        encoded_name = quote(test_name)
        response = self.client.get(f'{self.url}?name={encoded_name}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = json.loads(response.content)
        self.assertEqual(data['message'], f'Hello, {test_name}!') 