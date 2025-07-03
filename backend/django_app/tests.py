from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse

class UrlsViewTest(TestCase):

    def setUp(self):
        """Set up test client before running each test."""
        self.client = Client()

    def test_hello_default(self):
        """Test GET request with default values."""
        response = self.client.get('/hello/')  

        self.assertEqual(response.status_code, 200)  # Ensure response is OK
        self.assertContains(response, "call me, Ishamel")  # Check default name
        self.assertContains(response, "48")  # Check default weight
        self.assertContains(response, "1.5")  # Check default height

    def test_hello_with_params(self):
        """Test GET request with query parameters."""
        response = self.client.get('/hello/', {"name": "Pavan", "weight": "60", "height": "1.75"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "call me, Pavan")
        self.assertContains(response, "60")
        self.assertContains(response, "1.75")

    def test_hello_invalid_input(self):
        """Test handling of invalid weight/height input."""
        response = self.client.get('/hello/', {"weight": "abc", "height": "xyz"})

        self.assertEqual(response.status_code, 400)  # Expect a bad request
        self.assertContains(response, "Invalid input", status_code=400)
