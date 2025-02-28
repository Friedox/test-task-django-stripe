import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from payments.models import Item

class PaymentsTestCase(TestCase):
    def setUp(self):
        # Create a sample item for testing
        self.item = Item.objects.create(
            name="Test Item",
            description="This is a test item.",
            price=100
        )
        self.client = Client()

    def test_item_detail_view(self):
        """
        Test that the /item/<id>/ endpoint returns a valid HTML page with item details.
        """
        url = reverse('item_detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)
        self.assertContains(response, self.item.description)

    @patch('payments.views.stripe.checkout.Session.create')
    def test_buy_endpoint(self, mock_create):
        """
        Test that the /buy/<id>/ endpoint returns a JSON response with a session id.
        We patch stripe.checkout.Session.create to avoid making an actual API call.
        """
        # Configure the mock to return an object with an 'id' attribute.
        mock_create.return_value = type('Session', (), {'id': 'sess_test_123'})()

        url = reverse('buy', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('id', data)
        self.assertEqual(data['id'], 'sess_test_123')