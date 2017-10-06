import json
from tests.basetest import BaseTestCase

class Recipes(BaseTestCase):
    def test_register(self):
        response = self.client.post('/auth/register', data=self.user)
        self.assertEqual(response.status, "200 OK")